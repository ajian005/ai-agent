# Site Reliability Engineer (SRE) Skills

The SRE applies software engineering principles to infrastructure and operations problems. They ensure systems are reliable, scalable, and efficient.

## Role Definition
Focuses on SLIs/SLOs, error budgets, automation, incident management, and capacity planning.

## Skills & Tools

### 1. Reliability Engineering
Defining and measuring reliability.

- **Tool: SLI (Service Level Indicator)**
  - *Description*: A quantitative measure of some aspect of the level of service (e.g., latency, error rate).
  - *Practice*: Choose the right metrics that reflect user experience.
  - *Agent Prompt*: "Define SLIs for the 'Search' service (Availability and Latency)."

- **Tool: SLO (Service Level Objective)**
  - *Description*: A target value or range of values for a service level that is measured by an SLI.
  - *Practice*: Set realistic targets (e.g., 99.9% availability).
  - *Agent Prompt*: "Calculate the error budget for a 99.9% SLO over 30 days."

- **Tool: Error Budgets**
  - *Description*: The amount of error that your service can accumulate without violating the SLO.
  - *Practice*: Use the budget to balance innovation (velocity) vs. reliability.
  - *Agent Prompt*: "Draft a policy for what happens when the error budget is exhausted."

### 2. Automation & Toil Reduction
Replacing manual work with code.

- **Tool: Python / Go Scripting**
  - *Description*: Automating operational tasks.
  - *Practice*: Write scripts to automate backups, cleanups, or failovers.
  - *Agent Prompt*: "Write a Python script to automatically rotate API keys."

- **Tool: Runbooks / Playbooks**
  - *Description*: Documentation (often executable) for handling incidents.
  - *Practice*: Create step-by-step guides for common alerts.
  - *Agent Prompt*: "Create a runbook for handling a 'High CPU' alert."

### 3. Incident Management
Handling and learning from failures.

- **Tool: Blameless Post-Mortems**
  - *Description*: Analyzing incidents without assigning blame.
  - *Practice*: Focus on process and system improvements.
  - *Agent Prompt*: "Draft a post-mortem template focusing on timeline and root cause."

- **Tool: Chaos Engineering**
  - *Description*: Proactively testing system resilience.
  - *Practice*: Inject faults (latency, crashes) to verify recovery.
  - *Agent Prompt*: "Plan a Chaos Monkey experiment to test pod resilience."

### 4. Capacity Planning
Ensuring the system can handle future load.

- **Tool: Load Testing (k6 / Locust)**
  - *Description*: Simulating traffic to find limits.
  - *Practice*: Determine the breaking point of the system.
  - *Agent Prompt*: "Write a k6 script to simulate a spike in traffic."

- **Tool: Auto-scaling Configuration**
  - *Description*: Automatically adjusting resources based on demand.
  - *Practice*: Configure HPA (Horizontal Pod Autoscaler) or Cluster Autoscaler.
  - *Agent Prompt*: "Configure HPA rules based on custom metrics (queue depth)."
