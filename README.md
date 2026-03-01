# Medical-Clinic-Queue-Simulation

# 🏥 Medical Clinic Multi-Channel Queue Simulation

**Discrete-Event Simulation | Modeling & Simulation Project**

This project implements a Discrete-Event Simulation (DES) model of a medical clinic serving multiple patient categories under priority-based service rules.

The system is modeled using Python to analyze queue behavior, waiting times, doctor utilization, and the impact of adding an extra doctor.

## 📌 Problem Description

The clinic serves three types of patients:

- 🧑 Middle-age patients
- 👴 Elderly patients
- 🚑 Emergency patients (highest priority)

The clinic operates with:

- **2 doctors** (base system)
- Priority service rules
- Probabilistic inter-arrival times
- Probabilistic examination times
- Balking behavior (some middle-age patients may leave if waiting > 30 minutes)

Emergency patients always receive priority when a doctor becomes available.

Because of randomness in:

- Arrival times
- Service times
- Patient categories
- Patient behavior

The system is analyzed using discrete-event simulation instead of analytical modeling.

## 🎯 Objectives

The simulation evaluates:

- Average examination time per patient type
- Average waiting time per patient category
- Overall system waiting time
- Maximum queue length per doctor
- Probability of waiting
- Doctor idle time portion
- Comparison between theoretical and experimental averages
- Impact of adding a third doctor

## ⚙️ System Modeling Approach

The simulation is implemented using:

- Random sampling from discrete probability distributions
- Priority-based queue logic
- Separate queues for:
  - Middle-age patients
  - Elderly patients
  - Emergency patients
- Doctor assignment rules based on specialization and availability
- Balking behavior simulation
- Performance metric collection

## 🧠 Key Features Implemented

- Multi-channel queue system
- Priority queue handling
- Discrete probability distributions
- Balking behavior modeling
- Idle time tracking
- Theoretical vs experimental comparison
- Scenario comparison (2 doctors vs 3 doctors)
- Visualization using Matplotlib

## 📊 Performance Metrics Calculated

- Average waiting time (per patient type)
- Waiting probability
- Maximum queue length
- Average examination time
- Doctor idle portion
- Inter-arrival time validation
- System comparison before & after adding extra doctor

## 🛠️ Technologies Used

- Python
- NumPy
- Matplotlib
- Collections (deque)
- Random module

## 📈 Simulation Comparison

The project compares:

| Scenario | Doctors | Result |
|----------|---------|--------|
| Original System | 2 Doctors | Higher waiting times |
| Improved System | 3 Doctors | Reduced waiting & better utilization |

The simulation clearly demonstrates the operational improvement after adding an extra doctor.

## 🚀 How to Run

```bash
pip install numpy matplotlib
python simulation.py
```

The script will:

- Print statistical results
- Compare scenarios
- Display a performance comparison graph

## 📚 Academic Context

This project was developed as part of a **Modeling and Simulation** course, applying discrete-event simulation principles to a real-world healthcare service system.

## 🎯 Learning Outcomes

- Discrete-event simulation modeling
- Multi-server queue systems
- Priority scheduling logic
- Performance evaluation metrics
- Scenario analysis
- System improvement evaluation

## 📁 Project Structure

medical-clinic-simulation/
 - simulation.py          # Main simulation script
 - README.md              # Project documentation
 - requirements.txt       # Dependencies
 - results/               # Output graphs and data
    - comparison_plot.png
    - simulation_results.txt

## 📊 Sample Output

The simulation generates output similar to:
SIMULATION RESULTS (2 DOCTORS) 
   - Average waiting time: 12.5 minutes
   - Waiting probability: 0.45
   - Max queue length: 8 patients
   - Doctor idle time: 18%

SIMULATION RESULTS (3 DOCTORS)
   - Average waiting time: 4.2 minutes
   - Waiting probability: 0.18
   - Max queue length: 3 patients
   - Doctor idle time: 32%



## 🤝 Contributing

Feel free to fork this project, submit issues, or make pull requests for improvements.
    
