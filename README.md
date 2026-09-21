# Battery Optimization System

## Overview

Battery Optimization System is a Python-based AI-powered system
that monitors laptop battery and system resource usage, identifies
the current workload, predicts battery behavior, and provides
actionable battery optimization recommendations.

The system collects real-time information such as battery level,
CPU usage, RAM usage, screen brightness, active applications,
and workload information.

It evaluates the current battery pressure and generates
recommendations based on the system condition.

The system is designed with Snapdragon-powered HP PCs in mind,
with future optimization focused on efficient, low-latency,
on-device AI inference.

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
- Battery behavior prediction
- Application-level resource analysis
- Battery optimization recommendations
- Synthetic data generation for model training
- Machine learning-based workload classification
- Battery usage and drain analysis
- Real-world testing and evaluation
- Interactive web dashboard

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
- Application CPU and RAM usage
- Workload type

## Workload Types

- Coding
- Light
- Video
- WhatsApp

## Machine Learning

The project uses machine learning to classify workload conditions
and analyze battery-related behavior.

Real-world testing achieved an accuracy of approximately 75%.

Five-fold cross-validation produced a mean accuracy of
approximately 76.4%.

The machine learning components are used to understand workload
conditions and support battery-related prediction and
optimization decisions.

## Battery Optimization

The system calculates a battery pressure score using battery level
and system resource conditions.

Based on the detected battery pressure and workload, the system
provides recommendations such as:

- Reduce screen brightness
- Close unused applications
- Close applications with high resource usage
  when they are not needed
- Reduce unnecessary background processes
- Enable Battery Saver / power-saving mode
- Apply workload-specific recommendations

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
- Enable Battery Saver / power-saving mode

## Project Structure

- `battery_logger_v3.py` – real-time system monitoring
- `battery_optimizer.py` – battery pressure and
  recommendation logic
- `optimization_controller.py` – optimization control logic
- `generate_synthetic.py` – synthetic data generation
- `analyse_battery.py` – battery and workload analysis
- `app_features_test.py` – application feature testing
- `running_apps.py` – active application detection
- `battery_test.py` – battery-related testing
- `train_models.py` – machine learning model training
- `backend.py` – backend API for the dashboard
- `frontend.html` – dashboard interface
- `frontend/` – frontend resources
- CSV files – collected, synthetic, and processed datasets
- PKL files – trained machine learning models
  and feature data
- `project_results.txt` – project results and observations
- `Requirements.txt` – Python dependencies

## Technologies

- Python
- FastAPI
- HTML
- CSS
- JavaScript
- Pandas
- NumPy
- Scikit-learn
- Psutil
- Machine Learning
- CSV-based data processing

## Prototype

The project includes a web-based dashboard that displays:

- Current battery level
- Battery pressure
- Estimated remaining time
- CPU usage
- RAM usage
- Detected workload
- Battery drain rate
- Predicted battery level
- Active applications
- AI-generated battery recommendations

The dashboard is designed to provide users with a simple view
of their current battery condition and actionable
optimization suggestions.

## Snapdragon Optimization

The solution is designed with Snapdragon-powered HP PCs
in mind.

The current prototype performs local system monitoring,
workload analysis, machine learning inference,
and recommendation generation.

Future optimization will focus on:

- Efficient on-device AI inference
- Low-latency processing
- Reduced dependence on cloud processing
- Optimization of machine learning models
  for Snapdragon hardware
- Exploring Qualcomm AI Hub-compatible model optimization
- Hardware-aware battery optimization

## Future Scope

- Improve prediction accuracy using a larger real-world dataset
- Add personalized battery optimization
- Add automatic power-saving actions
- Support more workload categories
- Improve application-level power analysis
- Improve battery prediction using longer-term usage history
- Optimize machine learning inference for
  Snapdragon-powered HP PCs
- Explore Qualcomm AI Hub-compatible model deployment
- Develop more hardware-aware optimization strategies

## Project Goal

The goal of Battery Optimization System is to move beyond
simply displaying a battery percentage by helping users
understand why their battery is draining and what actions
they can take to extend battery life.
