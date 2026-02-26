# MLOps Engineer Skills

The MLOps Engineer sits at the intersection of Machine Learning, DevOps, and Data Engineering. They operationalize ML models.

## Role Definition
Focuses on model lifecycle management, automated retraining, model monitoring, and scalable inference.

## Skills & Tools

### 1. Model Lifecycle Management
Tracking experiments and models.

- **Tool: MLflow**
  - *Description*: Platform for the ML lifecycle (tracking, projects, models, registry).
  - *Practice*: Log parameters, metrics, and artifacts; register versioned models.
  - *Agent Prompt*: "Set up an MLflow tracking server and log a training run."

- **Tool: DVC (Data Version Control)**
  - *Description*: Version control for data and models.
  - *Practice*: Track datasets and model files in Git-compatible way.
  - *Agent Prompt*: "Initialize DVC in a project and track the 'data/raw.csv' file."

### 2. ML Pipelines & Orchestration
Automating the ML workflow.

- **Tool: Kubeflow / Airflow**
  - *Description*: Orchestrating complicated ML workflows on Kubernetes.
  - *Practice*: Define pipeline steps (ingest, preprocess, train, eval, deploy).
  - *Agent Prompt*: "Design a Kubeflow pipeline for daily model retraining."

- **Tool: TFX (TensorFlow Extended)**
  - *Description*: Production-scale machine learning platform.
  - *Practice*: Build pipelines for TensorFlow models.
  - *Agent Prompt*: "Create a TFX pipeline component for data validation."

### 3. Model Serving & Deployment
Exposing models as services.

- **Tool: TensorFlow Serving / TorchServe**
  - *Description*: Flexible, high-performance serving systems.
  - *Practice*: Deploy models for real-time inference via gRPC/REST.
  - *Agent Prompt*: "Create a Dockerfile to serve a model using TensorFlow Serving."

- **Tool: Seldon Core / KServe**
  - *Description*: Kubernetes-native model serving.
  - *Practice*: Handle advanced serving patterns (Canary, A/B testing, Shadowing).
  - *Agent Prompt*: "Define a SeldonDeployment manifest for A/B testing two models."

### 4. Monitoring & Observability
Ensuring models perform well in production.

- **Tool: Drift Detection**
  - *Description*: Identifying when production data diverges from training data.
  - *Practice*: Monitor for Data Drift (input changes) and Concept Drift (relationship changes).
  - *Agent Prompt*: "Implement a drift detection check using Evidently AI."

- **Tool: Prometheus & Grafana for ML**
  - *Description*: Monitoring system metrics and custom model metrics.
  - *Practice*: Dashboard for prediction latency, throughput, and accuracy.
  - *Agent Prompt*: "Create a Grafana dashboard to monitor model prediction confidence scores."
