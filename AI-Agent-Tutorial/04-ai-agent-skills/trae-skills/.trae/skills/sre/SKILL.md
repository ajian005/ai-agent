---
name: "sre"
description: "Ensures site reliability and scalability. Invoke when defining SLOs, automating runbooks, or managing incidents."
---

# Site Reliability Engineer (SRE)

This skill applies software engineering to operations problems, focusing on reliability, scalability, and efficiency.

## Core Responsibilities

1.  **Reliability**: Defining and monitoring SLIs and SLOs.
2.  **Incident Management**: Responding to and learning from failures.
3.  **Automation**: Eliminating toil through code.
4.  **Capacity Planning**: Ensuring resources meet demand.

## Key Concepts

### 1. Reliability Metrics
-   **SLI (Indicator)**: What we measure (e.g., latency).
-   **SLO (Objective)**: The target (e.g., < 200ms).
-   **SLA (Agreement)**: The promise to customers (with penalties).

### 2. Error Budgets
-   The allowance for unreliability. If budget remains, ship features; if exhausted, focus on stability.

## Workflow

When invoked, this skill will guide you through:

1.  **Definition**: Set up SLIs and SLOs for a service.
2.  **Automation**: Write scripts to handle common operational tasks.
3.  **Response**: Follow runbooks during an incident.
4.  **Review**: Conduct a post-mortem to prevent recurrence.

## Usage Scenarios

-   **New Service**: "Define reliability targets." -> SRE Skill: "Set an SLO of 99.9% availability and define the error budget."
-   **Alerting**: "Too many false alarms." -> SRE Skill: "Tune alert thresholds and group related alerts."
-   **Toil**: "I manually restart this server every day." -> SRE Skill: "Write a cron job or Kubernetes liveness probe to handle it."

## Output Format

-   **SLO Definition**: Metrics and targets.
-   **Runbook**: Step-by-step incident response guide.
-   **Post-Mortem**: Incident analysis report.
