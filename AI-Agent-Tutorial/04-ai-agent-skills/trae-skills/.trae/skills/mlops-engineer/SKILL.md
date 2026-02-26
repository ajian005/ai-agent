---
name: "mlops-engineer"
description: "Operationalizes ML models. Invoke when setting up training pipelines, model tracking, or serving infrastructure."
---

# MLOps Engineer

This skill bridges the gap between data science and operations, ensuring ML models are reliable, scalable, and maintainable in production.

## Core Responsibilities

1.  **Pipeline Automation**: Automating data ingestion, training, and deployment.
2.  **Model Tracking**: Versioning data, code, and model artifacts.
3.  **Serving**: Deploying models for inference.
4.  **Monitoring**: Tracking model performance and data drift.

## Key Technologies

### 1. Orchestration
-   **Kubeflow**: Kubernetes-native ML platform.
-   **Airflow**: Workflow orchestration.

### 2. Lifecycle Management
-   **MLflow**: Tracking experiments and models.
-   **DVC**: Data Version Control.

### 3. Serving
-   **TensorFlow Serving / TorchServe**: High-performance inference.
-   **Seldon Core**: Advanced serving patterns.

## Workflow

When invoked, this skill will guide you through:

1.  **Setup**: Configure the experiment tracking server.
2.  **Pipeline**: Define steps for training and evaluation.
3.  **Registry**: Version the best model.
4.  **Deployment**: Serve the model via REST/gRPC.
5.  **Monitor**: Set up alerts for drift.

## Usage Scenarios

-   **Tracking**: "Log this training run." -> MLOps Skill: "Use `mlflow.log_param` and `mlflow.log_metric`."
-   **Automation**: "Retrain the model weekly." -> MLOps Skill: "Create an Airflow DAG to trigger the pipeline."
-   **Deployment**: "Deploy to Kubernetes." -> MLOps Skill: "Create a deployment manifest using Seldon Core."

## Output Format

-   **Pipeline Code**: Python script or DAG definition.
-   **Docker Config**: Dockerfile for serving.
-   **Monitoring Config**: Dashboard definition.
