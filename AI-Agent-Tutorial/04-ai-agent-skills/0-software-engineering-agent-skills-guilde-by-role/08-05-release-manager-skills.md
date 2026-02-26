# Release Manager Skills

The Release Manager oversees the software release lifecycle, ensuring that updates are deployed to production smoothly and safely.

## Role Definition
Focuses on release planning, versioning, environment management, and change control.

## Skills & Tools

### 1. Release Planning
Scheduling and coordinating releases.

- **Tool: Release Calendar**
  - *Description*: A schedule of upcoming releases and code freezes.
  - *Practice*: Coordinate with dev, QA, and ops teams.
  - *Agent Prompt*: "Create a release calendar for Q3 including code freeze dates."

- **Tool: Jira (Release Module)**
  - *Description*: Tracking scope and status of releases.
  - *Practice*: Group tickets into versions/releases.
  - *Agent Prompt*: "Generate release notes from Jira tickets for version 2.1."

### 2. Version Control & Branching
Managing the code flow.

- **Tool: Git Flow / Trunk Based Development**
  - *Description*: Branching strategies.
  - *Practice*: Manage release branches and tagging.
  - *Agent Prompt*: "Explain the Git Flow process for creating a hotfix branch."

- **Tool: Semantic Versioning (SemVer)**
  - *Description*: Standard versioning scheme (Major.Minor.Patch).
  - *Practice*: Determine version numbers based on changes.
  - *Agent Prompt*: "Determine the next version number after a breaking API change."

### 3. Deployment Strategies
Pushing code to users.

- **Tool: Blue-Green Deployment**
  - *Description*: Running two identical environments to switch traffic.
  - *Practice*: Minimize downtime and risk.
  - *Agent Prompt*: "Design a Blue-Green deployment strategy for the web application."

- **Tool: Canary Releases**
  - *Description*: Rolling out changes to a small subset of users first.
  - *Practice*: Monitor for errors before full rollout.
  - *Agent Prompt*: "Define the criteria for promoting a canary release to 100% traffic."

### 4. Change Management
Ensuring compliance and stability.

- **Tool: CAB (Change Advisory Board)**
  - *Description*: A group that approves changes.
  - *Practice*: Prepare change requests with rollback plans.
  - *Agent Prompt*: "Draft a Change Request for the database schema migration."

- **Tool: Rollback Plans**
  - *Description*: Procedures to revert a failed release.
  - *Practice*: Ensure quick recovery from bad deployments.
  - *Agent Prompt*: "Write a rollback procedure for a failed Docker deployment."
