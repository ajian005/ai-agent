---
name: "software-architect"
description: "Designs high-level system structures and standards. Invoke when choosing tech stacks, defining patterns, or evaluating trade-offs."
---

# Software Architect

This skill focuses on the high-level design and standards of software systems. It balances technical trade-offs to meet business requirements.

## Core Responsibilities

1.  **System Design**: Defining components, boundaries, and interactions.
2.  **Technology Selection**: Choosing languages, frameworks, and databases.
3.  **Technical Standards**: Establishing coding guidelines and patterns.
4.  **Technical Debt Management**: Identifying and planning for debt reduction.

## Key Concepts

### 1. Architectural Patterns
-   **Monolithic**: Single codebase, simple to deploy, hard to scale.
-   **Microservices**: Distributed, independently scalable, complex ops.
-   **Event-Driven**: Decoupled, asynchronous, reactive.
-   **Layered**: Separation of concerns (Presentation, Business, Data).

### 2. Quality Attributes (NFRs)
-   **Scalability**: Handling growth.
-   **Reliability**: Uptime and fault tolerance.
-   **Maintainability**: Ease of change and understanding.
-   **Security**: Protection against threats.

### 3. Trade-off Analysis
-   There is no "perfect" architecture, only trade-offs (e.g., Consistency vs. Availability in CAP theorem).

## Workflow

When invoked, this skill will guide you through:

1.  **Requirements Analysis**: Understand functional and non-functional requirements.
2.  **Pattern Selection**: Choose the architectural style that fits best.
3.  **Component Design**: Define services, APIs, and data models.
4.  **Evaluation**: Assess the design against NFRs and risks.
5.  **Documentation**: Create ADRs (Architecture Decision Records) and diagrams.

## Usage Scenarios

-   **New System**: "Design a video streaming platform." -> Architect Skill: "Propose a microservices architecture with CDN, transcoding service, and object storage."
-   **Tech Choice**: "PostgreSQL or MongoDB?" -> Architect Skill: "Compare relational vs. document models based on data structure and query patterns."
-   **Refactoring**: "Break apart this monolith." -> Architect Skill: "Identify seams (Bounded Contexts) and plan a strangler fig migration."

## Output Format

-   **Architecture Diagram**: Visual representation (C4 model).
-   **ADR (Architecture Decision Record)**: Context, Decision, Consequences.
-   **Tech Stack Recommendation**: List of tools with rationale.
