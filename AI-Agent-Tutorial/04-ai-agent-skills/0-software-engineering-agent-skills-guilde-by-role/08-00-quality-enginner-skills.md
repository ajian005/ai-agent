# Quality Engineer Skills

The Quality Engineer (QA/QE) is responsible for ensuring the software meets the required standards of quality, reliability, and performance before release.

## Role Definition
Focuses on test planning, automation, defect tracking, and preventing bugs.

## Skills & Tools

### 1. Test Planning & Strategy
Defining what and how to test.

- **Tool: Test Plan**
  - *Description*: Document describing the scope, approach, resources, and schedule of testing.
  - *Practice*: Define test objectives and criteria for success.
  - *Agent Prompt*: "Draft a Test Plan for the upcoming 'Mobile App' release."

- **Tool: Test Case Management**
  - *Description*: Organizing test cases (TestRail, Xray, Zephyr).
  - *Practice*: Write clear, reproducible test steps and expected results.
  - *Agent Prompt*: "Write 5 test cases for the 'Password Reset' functionality."

### 2. Test Automation
Automating repetitive testing tasks.

- **Tool: E2E Testing Frameworks**
  - *Description*: Tools for end-to-end testing (Selenium, Cypress, Playwright).
  - *Practice*: Automate critical user journeys.
  - *Agent Prompt*: "Write a Cypress script to test the 'Checkout' flow."

- **Tool: API Testing**
  - *Description*: Testing API endpoints (Postman, REST Assured).
  - *Practice*: Verify response codes, bodies, and performance.
  - *Agent Prompt*: "Create a Postman collection to test the 'User API' endpoints."

### 3. Defect Management
Tracking and resolving issues.

- **Tool: Bug Tracking System**
  - *Description*: Logging and managing defects (Jira, GitHub Issues).
  - *Practice*: Report bugs with detailed reproduction steps, logs, and screenshots.
  - *Agent Prompt*: "Write a bug report for a crash occurring on the 'Profile Page'."

- **Tool: Root Cause Analysis**
  - *Description*: Identifying the underlying cause of a defect.
  - *Practice*: Use "5 Whys" or Fishbone diagrams to prevent recurrence.
  - *Agent Prompt*: "Perform a root cause analysis for the production outage on Sunday."

### 4. Performance & Load Testing
Verifying system stability under stress.

- **Tool: Load Testing Tools**
  - *Description*: Simulating traffic (JMeter, k6, Gatling).
  - *Practice*: Measure response times and throughput under high load.
  - *Agent Prompt*: "Design a JMeter test plan to simulate 10,000 concurrent users."

- **Tool: Chaos Engineering**
  - *Description*: Experimenting on a system to build confidence in its capability to withstand turbulent conditions (Chaos Monkey).
  - *Practice*: Intentionally introduce failures to test resilience.
  - *Agent Prompt*: "Plan a chaos engineering experiment to test database failover."
