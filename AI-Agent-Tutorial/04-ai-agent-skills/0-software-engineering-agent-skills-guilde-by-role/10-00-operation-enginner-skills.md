# Operation Engineer Skills

The Operation Engineer (Ops/SRE) is responsible for the deployment, management, and monitoring of the software infrastructure and applications.

## Role Definition
Focuses on reliability, automation, infrastructure as code (IaC), and incident response.

## Skills & Tools

### 1. Infrastructure as Code (IaC)
Managing infrastructure through code.

- **Tool: Terraform / Ansible**
  - *Description*: Tools for provisioning and configuration management.
  - *Practice*: Define infrastructure resources (servers, networks) in code files.
  - *Agent Prompt*: "Write a Terraform configuration to provision an AWS EC2 instance."

- **Tool: Container Orchestration**
  - *Description*: Managing containerized applications (Kubernetes, Docker Swarm).
  - *Practice*: Deploy, scale, and manage container clusters.
  - *Agent Prompt*: "Create a Kubernetes Deployment manifest for the 'Web Service'."

### 2. CI/CD (Continuous Integration/Continuous Deployment)
Automating the software delivery process.

- **Tool: CI/CD Pipelines**
  - *Description*: Automation servers (Jenkins, GitLab CI, GitHub Actions).
  - *Practice*: Automate build, test, and deployment steps.
  - *Agent Prompt*: "Create a GitHub Actions workflow to build and push a Docker image."

- **Tool: Release Management**
  - *Description*: Strategies for deploying code (Blue-Green, Canary).
  - *Practice*: Minimize downtime and risk during deployments.
  - *Agent Prompt*: "Design a Canary deployment strategy for the new API version."

### 3. Monitoring & Observability
Keeping an eye on system health.

- **Tool: Monitoring Stacks**
  - *Description*: Collecting and visualizing metrics (Prometheus, Grafana, ELK Stack).
  - *Practice*: Set up dashboards and alerts for key performance indicators (KPIs).
  - *Agent Prompt*: "Create a Grafana dashboard to monitor HTTP error rates."

- **Tool: Log Management**
  - *Description*: Aggregating and analyzing logs (Splunk, Fluentd).
  - *Practice*: Centralize logs for easier debugging and auditing.
  - *Agent Prompt*: "Configure Fluentd to ship application logs to Elasticsearch."

### 4. Incident Response
Handling outages and issues.

- **Tool: Incident Management**
  - *Description*: Processes for handling incidents (PagerDuty, Opsgenie).
  - *Practice*: Acknowledge, triage, and resolve alerts within SLA.
  - *Agent Prompt*: "Draft an Incident Response Playbook for a 'Database Down' scenario."

- **Tool: Post-Mortem**
  - *Description*: Analyzing incidents after they occur.
  - *Practice*: Document what happened, why, and how to prevent it.
  - *Agent Prompt*: "Write a Post-Mortem report for the service outage on [Date]."
