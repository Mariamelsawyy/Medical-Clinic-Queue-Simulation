import random
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# Distributions
inter_arrival_times = [2, 5, 7, 10]
inter_arrival_probs = [0.10, 0.30, 0.25, 0.35]

exam_times_normal = [5, 7, 10]
exam_probs_normal = [0.20, 0.30, 0.50]

exam_times_emergency = [7, 10, 15]
exam_probs_emergency = [0.20, 0.50, 0.30]


def random_from_distribution(values, probabilities):
    r = random.random()
    cumulative = 0
    for value, prob in zip(values, probabilities):
        cumulative += prob
        if r <= cumulative:
            return value
    return values[-1]  

def get_patient_type():
    r = random.random()
    if r <= 0.7:
        return "middle"
    elif r <= 0.9:
        return "elderly"
    else:
        return "emergency"


# Patient Generation
def generate_patients(n):
    patients = []
    current_time = 0

    for i in range(n):
        ia = random_from_distribution(inter_arrival_times, inter_arrival_probs)
        current_time += ia
        p_type = get_patient_type()

        if p_type == "emergency":
            exam = random_from_distribution(exam_times_emergency, exam_probs_emergency)
        else:
            exam = random_from_distribution(exam_times_normal, exam_probs_normal)

        patients.append({
            "id": i + 1,
            "type": p_type,
            "arrival_time": current_time,
            "exam_time": exam
        })

    return patients


# Simulation
def simulate_clinic(patients, extra_doctor=False):
    queue_middle = deque()
    queue_elderly = deque()
    queue_emergency = deque()

    doctors = [
        {"busy": False, "finish": 0, "idle": 0, "last_time": 0, "max_q": 0},
        {"busy": False, "finish": 0, "idle": 0, "last_time": 0, "max_q": 0}
    ]

    if extra_doctor:
        doctors.append(
            {"busy": False, "finish": 0, "idle": 0, "last_time": 0, "max_q": 0}
        )

    waiting_times = {"middle": [], "elderly": [], "emergency": []}
    current_time = 0

    for patient in patients:
        current_time = patient["arrival_time"]

        # free doctors and accumulate idle time
        for d in doctors:
            if d["busy"] and d["finish"] <= current_time:
                d["busy"] = False
                d["last_time"] = d["finish"]

            if not d["busy"]:
                d["idle"] += current_time - d["last_time"]
                d["last_time"] = current_time

        patient["queue_entry"] = current_time

        if patient["type"] == "emergency":
            queue_emergency.append(patient)
        elif patient["type"] == "middle":
            queue_middle.append(patient)
        else:
            queue_elderly.append(patient)

        doctors[0]["max_q"] = max(doctors[0]["max_q"], len(queue_middle))
        doctors[1]["max_q"] = max(doctors[1]["max_q"], len(queue_elderly))

        for d in doctors:
            if not d["busy"]:
                p = None

                if queue_emergency:
                    p = queue_emergency.popleft()
                elif d == doctors[0] and queue_middle:
                    p = queue_middle.popleft()
                elif d == doctors[1] and queue_elderly:
                    p = queue_elderly.popleft()
                elif d == doctors[1] and queue_middle:
                    p = queue_middle.popleft()
                elif extra_doctor and d == doctors[2] and queue_middle:
                    p = queue_middle.popleft()

                if p:
                    wait = current_time - p["queue_entry"]

                    # Balking logic
                    if p["type"] == "middle" and wait > 30:
                        if random.random() <= 0.3:
                            continue

                    waiting_times[p["type"]].append(wait)
                    d["busy"] = True
                    d["finish"] = current_time + p["exam_time"]

    total_time = patients[-1]["arrival_time"]
    for d in doctors:
        if not d["busy"]:
            d["idle"] += total_time - d["last_time"]

    return waiting_times, doctors


# Run Simulation
patients = generate_patients(100)
for p in patients[:20]:
     
     print(p)

wt_normal, doctors_normal = simulate_clinic(patients, extra_doctor=False)
wt_extra, doctors_extra = simulate_clinic(patients, extra_doctor=True)


# Results
def print_results(title, waiting_times, doctors, patients):
    print("\n", title)

    for t in waiting_times:
        print(f"Average waiting time ({t}): {np.mean(waiting_times[t]):.2f}")

    for i, d in enumerate(doctors, start=1):
        print(f"Doctor {i} max queue length: {d['max_q']}")

    exam_times = {"middle": [], "elderly": [], "emergency": []}
    for p in patients:
        exam_times[p["type"]].append(p["exam_time"])

    for t in exam_times:
        print(f"Average exam time ({t}): {np.mean(exam_times[t]):.2f}")


print_results("Original System (2 Doctors)", wt_normal, doctors_normal, patients)
print_results("With Extra Doctor", wt_extra, doctors_extra, patients)


# Statistics
def theoretical_mean(values, probs):
    return sum(v * p for v, p in zip(values, probs))


print("\nTheoretical exam time (middle & elderly):",
      theoretical_mean(exam_times_normal, exam_probs_normal))
print("Theoretical exam time (emergency):",
      theoretical_mean(exam_times_emergency, exam_probs_emergency))
print("Theoretical inter-arrival time:",
      theoretical_mean(inter_arrival_times, inter_arrival_probs))


def experimental_interarrival(patients):
    return np.mean([
        patients[i]["arrival_time"] - patients[i-1]["arrival_time"]
        for i in range(1, len(patients))
    ])


print(f"Experimental inter-arrival time:,{ experimental_interarrival(patients):.2f}")


def waiting_probability(waiting_times):
    for t in waiting_times:
        waited = sum(1 for w in waiting_times[t] if w > 0)
        total = len(waiting_times[t])
        print(f"Waiting probability ({t}):{waited / total if total > 0 else 0:.4f}")


print("\nWaiting probabilities (2 Doctors)")
waiting_probability(wt_normal)

print("\nWaiting probabilities (3 Doctors)")
waiting_probability(wt_extra)


def calculate_idle_time(patients, doctors):
    total_time = patients[-1]["arrival_time"]
    for i, d in enumerate(doctors, start=1):
        print(f"Doctor {i} idle portion:,{d["idle"] / total_time :.6f}")


print("\nIdle time (2 Doctors)")
calculate_idle_time(patients, doctors_normal)

print("\nIdle time (3 Doctors)")
calculate_idle_time(patients, doctors_extra)


# Graph
labels = wt_normal.keys()
normal_vals = [np.mean(wt_normal[k]) for k in labels]
extra_vals = [np.mean(wt_extra[k]) for k in labels]

x = np.arange(len(labels))
plt.bar(x - 0.2, normal_vals, width=0.4, label="2 Doctors")
plt.bar(x + 0.2, extra_vals, width=0.4, label="3 Doctors")
plt.xticks(x, labels)
plt.ylabel("Average Waiting Time")
plt.title("Effect of Adding an Extra Doctor")
plt.legend()
plt.show()
