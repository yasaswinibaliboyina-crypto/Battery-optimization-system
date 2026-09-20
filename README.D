# Battery Optimization System

## Overview

The Battery Optimization System is a Python-based system that monitors laptop battery and system resource usage and provides battery optimization recommendations.

The system collects battery level, CPU usage, RAM usage, screen brightness, active applications, and workload information. It then evaluates the current battery pressure and generates recommendations based on the system condition.

## Features

- Real-time battery monitoring
- CPU and RAM usage monitoring
- Screen brightness monitoring
- Active application detection
- Workload classification
- Battery pressure scoring
- Battery pressure levels:
  - Normal
  - Moderate
  - High
  - Critical
- Battery optimization recommendations
- Synthetic data generation for model training
- Machine learning based workload classification
- Battery usage and drain analysis
- Real-world testing and evaluation

## System Workflow

Laptop System
→ Data Collection
→ Workload Detection
→ Battery Prediction
→ Battery Pressure Evaluation
→ Optimization Recommendations

## Main Parameters

- Battery percentage
- CPU usage
- RAM usage
- Screen brightness
- Active application count
- Application usage
- Workload type

## Workload Types

- Coding
- Light
- Video
- WhatsApp

## Machine Learning

The project uses machine learning to classify workload conditions and analyze battery-related behavior.

Real-world testing achieved an accuracy of approximately 75%.

Five-fold cross-validation produced a mean accuracy of approximately 76.4%.

## Battery Optimization

The system calculates a battery pressure score using battery level and system resource conditions.

Depending on the detected pressure, the system provides recommendations such as:

- Reduce screen brightness
- Close unused applications
- Reduce unnecessary background processes
- Enable battery saver / power-saving mode

## Example

Battery: 15%  
CPU: 41.1%  
RAM: 61.8%  
Workload: Video

Battery Pressure: Critical  
Score: 80

Recommendations:

- Reduce screen brightness for video playback
- Reduce unnecessary background processes
- Enable battery saver / power-saving mode

## Project Structure

- `battery_logger_v3.py` – real-time system monitoring
- `battery_optimizer.py` – battery pressure and recommendation logic
- `generate_synthetic.py` – synthetic data generation
- `analyse_battery.py` – battery and workload analysis
- `app_features_test.py` – application feature testing
- `running_apps.py` – active application detection
- `battery_test.py` – battery-related testing
- CSV files – collected, synthetic, and processed datasets
- `project_results.txt` – project results and observations

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Psutil
- Machine Learning
- CSV-based data processing

## Future Scope

- Improve prediction accuracy using a larger real-world dataset
- Add personalized battery optimization
- Develop a graphical dashboard
- Add automatic power-saving actions
- Support more workload categories