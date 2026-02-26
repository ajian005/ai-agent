# Configuration Management Engineer Skills

The Configuration Management Engineer ensures consistency in system performance and functionality by managing configuration items and baselines.

## Role Definition
Focuses on version control, environment consistency, drift management, and configuration audits.

## Skills & Tools

### 1. Configuration Management Tools
Automating server state.

- **Tool: Ansible**
  - *Description*: Agentless automation tool.
  - *Practice*: Write Playbooks to configure servers.
  - *Agent Prompt*: "Write an Ansible playbook to install and configure PostgreSQL."

- **Tool: Puppet / Chef**
  - *Description*: Agent-based configuration management.
  - *Practice*: Define desired state (declarative) for infrastructure.
  - *Agent Prompt*: "Create a Puppet manifest to ensure the NTP service is running."

### 2. Infrastructure as Code (IaC)
Managing config as code.

- **Tool: Terraform**
  - *Description*: Provisioning infrastructure.
  - *Practice*: Manage cloud resources and state files.
  - *Agent Prompt*: "Explain how to manage Terraform state locking with S3 and DynamoDB."

- **Tool: CloudFormation**
  - *Description*: AWS native IaC.
  - *Practice*: Define AWS stacks in YAML/JSON.
  - *Agent Prompt*: "Create a CloudFormation template for an Auto Scaling Group."

### 3. Secret Management
Handling sensitive config.

- **Tool: HashiCorp Vault**
  - *Description*: Tool for secrets management.
  - *Practice*: Store and access secrets, tokens, and certificates securely.
  - *Agent Prompt*: "Configure an application to read database credentials from Vault."

- **Tool: AWS Secrets Manager**
  - *Description*: Managed service for secrets.
  - *Practice*: Rotate database secrets automatically.
  - *Agent Prompt*: "Set up automatic rotation for an RDS secret."

### 4. Drift Detection & Compliance
Ensuring systems stay configured.

- **Tool: Drift Detection**
  - *Description*: Identifying when manual changes occur.
  - *Practice*: Run regular checks against the baseline.
  - *Agent Prompt*: "Detect drift in the Terraform state for the production VPC."

- **Tool: Policy as Code (OPA)**
  - *Description*: Open Policy Agent.
  - *Practice*: Enforce policies (e.g., no public S3 buckets) on configuration.
  - *Agent Prompt*: "Write an OPA policy to deny creation of security groups with open port 22."
