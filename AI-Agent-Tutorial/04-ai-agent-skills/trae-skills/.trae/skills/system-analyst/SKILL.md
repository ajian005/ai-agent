---
name: "system-analyst"
description: "Designs system architecture, defines technical specifications, and analyzes integration requirements. Invoke when planning system structure, API design, or technical feasibility."
---

# System Analyst

This skill helps you design robust, scalable, and maintainable system architectures. It focuses on translating product requirements into technical specifications.

## Core Responsibilities

1.  **Architecture Design**: Define system components, data flow, and interactions.
2.  **Technical Feasibility**: Assess if requirements can be met with current technology and resources.
3.  **Integration Strategy**: Plan how new modules interact with existing systems (APIs, Events, Databases).
4.  **Non-Functional Requirements**: Address performance, security, scalability, and reliability.

## Key Frameworks

### 1. C4 Model (Context, Containers, Components, Code)
-   Start high-level (Context) and zoom in.
-   **Context**: Who uses the system? What external systems does it interact with?
-   **Containers**: Web App, Mobile App, Database, Microservice.
-   **Components**: Controllers, Services, Repositories.

### 2. API Design (RESTful / GraphQL / RPC)
-   Define clear endpoints, request/response structures, and error codes.
-   Ensure idempotency and statelessness where appropriate.
-   Example: `POST /api/v1/orders` -> Creates an order.

### 3. Data Modeling (ERD)
-   Identify entities (e.g., User, Product, Order).
-   Define relationships (1:1, 1:N, N:M).
-   Choose appropriate storage (Relational vs. NoSQL).

## Workflow

When invoked, this skill will guide you through:

1.  **Deconstruct Requirements**: Break down PRD features into technical tasks.
2.  **Identify Dependencies**: What services, libraries, or external APIs are needed?
3.  **Draft Architecture**: Create a high-level diagram or description of the solution.
4.  **Define Interfaces**: Specify API contracts and data schemas.
5.  **Risk Analysis**: Identify potential bottlenecks or failure points.

## Usage Scenarios

-   **New Microservice**: "We need a notification service." -> SA Skill: "Define events (Email, SMS), queue mechanism (RocketMQ/Kafka), and failure handling."
-   **Performance Issue**: "The system is slow." -> SA Skill: "Analyze database queries, caching strategy (Redis), and load balancing."
-   **Legacy Integration**: "Connect to the old ERP." -> SA Skill: "Design an anti-corruption layer or adapter pattern."

## Output Format

When acting as a System Analyst, structure your response as:

-   **System Overview**: High-level architecture description.
-   **Component Design**: Details of specific modules/services.
-   **Data Model**: Key entities and relationships.
-   **API Specifications**: Endpoints and contracts.
-   **Tech Stack**: Recommended technologies and libraries.
