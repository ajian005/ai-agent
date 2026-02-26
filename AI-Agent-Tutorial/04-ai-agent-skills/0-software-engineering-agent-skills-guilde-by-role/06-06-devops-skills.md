# DevOps Engineer Skills

The DevOps Engineer is responsible for the intersection of development (Dev) and operations (Ops), ensuring smooth software delivery, infrastructure management, and system reliability.

## Role Definition
Focuses on automation, CI/CD pipelines, infrastructure as code, cloud management, and observability.

## Skills & Tools

### 1. CI/CD (Continuous Integration & Deployment)
Automating the build, test, and release process.

- **Tool: GitHub Actions / GitLab CI**
  - *Description*: Platforms for automating software workflows.
  - *Practice*: Define workflows in YAML to build, test, and deploy code on every push.
  - *Agent Prompt*: "Create a GitHub Actions workflow to build a Docker image and push to ECR."

- **Tool: Jenkins**
  - *Description*: Open-source automation server.
  - *Practice*: Manage complex pipelines and integrations.
  - *Agent Prompt*: "Write a Jenkinsfile for a multi-stage build pipeline."

### 2. Infrastructure as Code (IaC)
Managing infrastructure using configuration files.

- **Tool: Terraform**
  - *Description*: Infrastructure provisioning tool.
  - *Practice*: Define cloud resources (VPCs, EC2, RDS) in HCL.
  - *Agent Prompt*: "Write Terraform code to provision an AWS S3 bucket with versioning enabled."

- **Tool: Ansible**
  - *Description*: Configuration management tool.
  - *Practice*: Automate server configuration and application deployment.
  - *Agent Prompt*: "Create an Ansible playbook to install Nginx and configure a static site."

### 3. Containerization & Orchestration
Packaging and managing applications.

- **Tool: Docker**
  - *Description*: Platform for developing, shipping, and running applications in containers.
  - *Practice*: Write Dockerfiles and docker-compose.yml files.
  - *Agent Prompt*: "Optimize this Dockerfile for a smaller image size."

- **Tool: Kubernetes (K8s)**
  - *Description*: Container orchestration system.
  - *Practice*: Manage deployments, services, and ingress resources.
  - *Agent Prompt*: "Create a Kubernetes Deployment manifest with a Horizontal Pod Autoscaler."

### 4. Observability & Monitoring
Ensuring system health and performance.

- **Tool: Prometheus & Grafana**
  - *Description*: Monitoring and visualization stack.
  - *Practice*: Collect metrics and create dashboards.
  - *Agent Prompt*: "Design a Grafana dashboard to monitor Kubernetes cluster CPU usage."

- **Tool: ELK Stack (Elasticsearch, Logstash, Kibana)**
  - *Description*: Log management and analysis.
  - *Practice*: Centralize and search logs for troubleshooting.
  - *Agent Prompt*: "Write a Logstash pipeline to parse Nginx access logs."
