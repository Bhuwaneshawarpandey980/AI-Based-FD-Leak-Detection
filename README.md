
# AI-Based File Descriptor Leak Detection Framework

## 1. Project Overview

The AI-Based File Descriptor Leak Detection Framework is an Operating Systems project that monitors Linux processes and uses machine learning to identify abnormal file descriptor usage.

A file descriptor leak occurs when a process opens files, sockets, pipes, or other resources but fails to close them when they are no longer required. Over time, this can exhaust available file descriptors and affect system reliability.

This project combines runtime monitoring, feature extraction, and a supervised Random Forest classifier to detect potential file descriptor leaks and generate alerts.

## 2. Objectives

- Monitor file descriptor usage of running Linux processes.
- Collect runtime information from `/proc/<PID>/fd`.
- Extract relevant features from process activity.
- Train a Random Forest classifier to distinguish normal behavior from potential leaks.
- Predict the behavior of a running process and report suspicious activity.
- Visualize file descriptor usage and growth patterns.

## 3. System Architecture

The system follows this workflow:

Linux Process  
↓  
Process Identification (PID)  
↓  
File Descriptor Monitoring (`/proc/<PID>/fd`)  
↓  
Runtime Data Collection  
↓  
Feature Extraction  
↓  
Dataset Preparation  
↓  
Random Forest Classifier  
↓  
Normal / Leak Detected  
↓  
Alert and Risk Assessment

## 4. Technologies Used

- **Programming Language:** Python
- **Operating System:** Linux / WSL2
- **Monitoring Interface:** Linux `/proc` filesystem
- **Machine Learning:** Random Forest classifier
- **Data Processing:** CSV datasets and extracted runtime features
- **Visualization:** Python plotting libraries
- **Development Environment:** Visual Studio Code
- **Version Control:** Git and GitHub

## 5. Features Extracted

The framework uses the following features:

- `fd_count` — current number of file descriptors.
- `fd_delta` — change in descriptor count.
- `fd_growth_rate` — rate of descriptor growth.
- `file_count` — number of file descriptors classified as files.
- `socket_count` — number of socket descriptors.
- `pipe_count` — number of pipe descriptors.
- `device_count` — number of device descriptors.
- `unknown_count` — number of descriptors that could not be classified.
- `fd_limit` — descriptor limit used for utilization calculations.
- `fd_utilization` — proportion of the descriptor limit being used.

## 6. Project Modules

| File | Purpose |
|---|---|
| `workloads.py` | Creates controlled normal and leak workloads. |
| `fd_monitor.py` | Monitors file descriptor usage. |
| `prepare_dataset.py` | Prepares data for model training. |
| `train_model.py` | Trains and evaluates the Random Forest model. |
| `predict_leak.py` | Performs leak prediction using the trained model. |
| `live_ai_monitor.py` | Monitors a running Linux process and predicts suspicious behavior. |
| `visualize_results.py` | Generates graphs for analyzing results. |

## 7. Dataset

The current recorded dataset contains:

- Normal observations: 33
- Controlled leak observations: 22
- Total observations: 55

The datasets are used to train and evaluate the supervised machine learning model.

**Note:** The dataset is relatively small and controlled. Additional observations from diverse workloads are needed to evaluate generalization more reliably.

## 8. Model and Evaluation

The project uses a supervised Random Forest classifier to classify observed process behavior as `NORMAL` or `LEAK DETECTED`.

The recorded evaluation on 14 held-out observations reported:

- Accuracy: 100%
- Precision: 1.00
- Recall: 1.00
- F1-score: 1.00

The recorded confusion matrix was:

| | Predicted Normal | Predicted Leak |
|---|---:|---:|
| Actual Normal | 8 | 0 |
| Actual Leak | 0 | 6 |

These results describe the current controlled evaluation only. They do not establish 100% accuracy on real-world workloads.

## 9. Generated Visualizations

The project generates graphs for comparing normal and leak behavior:

- `fd_count_comparison.png`
- `fd_growth_comparison.png`
- `socket_comparison.png`

These visualizations help examine differences in descriptor counts, growth patterns, and socket usage.

## 10. How to Run

### Prerequisites

- Linux or WSL2 with a working Linux environment.
- Python 3.
- Git.
- The Python dependencies required by the project.

### Step 1: Open the project

Open the project directory in your terminal or Visual Studio Code.

### Step 2: Activate the virtual environment

If you already created a virtual environment in Linux/WSL2, activate it:

```bash
source .venv/bin/activate
```

Use the actual environment directory name if yours differs.

### Step 3: Install dependencies

Install the Python packages required by your project. If you have a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

If you do not have that file, install the dependencies listed in your source code.

### Step 4: Prepare the dataset

```bash
python prepare_dataset.py
```

### Step 5: Train the model

```bash
python train_model.py
```

### Step 6: Run offline prediction

```bash
python predict_leak.py
```

### Step 7: Run live monitoring

```bash
python live_ai_monitor.py
```

Follow the program prompts and provide the PID of a running Linux process if requested. Monitor only processes you are authorized to inspect.

### Step 8: Generate visualizations

```bash
python visualize_results.py
```

**Important:** The commands above assume the scripts support these direct entry points. Follow any prompts in the scripts and check their source code if a command requires additional arguments or a particular execution order.

## 11. Limitations

- The current dataset is small and based on controlled workloads.
- Classification performance may vary across different applications and operating conditions.
- File descriptor growth alone does not prove a memory or resource leak.
- Monitoring permissions and the availability of process information depend on the Linux environment.
- More testing is required before using the framework for production monitoring.

## 12. Future Enhancements

- Collect more than 100 genuine observations for each class.
- Test with a wider variety of Linux applications and workloads.
- Improve detection of gradual leaks and changing usage patterns.
- Evaluate performance on independent datasets.
- Add historical monitoring, alert logging, and a real-time dashboard.

## 13. Conclusion

This project demonstrates how Linux runtime monitoring and supervised machine learning can be combined to identify potential file descriptor leaks. By collecting process-level features, training a Random Forest classifier, and providing live predictions and visualizations, the framework offers a foundation for further research into intelligent resource monitoring.

## 14. Author

**Project:** AI-Based File Descriptor Leak Detection Framework  
**Domain:** Operating Systems and Machine Learning  
**Environment:** Linux / WSL2 and Python
