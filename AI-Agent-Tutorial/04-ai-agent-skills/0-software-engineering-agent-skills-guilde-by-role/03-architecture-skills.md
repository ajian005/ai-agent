# Architecture Skills

The Software Architect is responsible for high-level design choices and dictating technical standards, including software coding standards, tools, and platforms.

## Role Definition
Focuses on system structure, scalability, trade-offs, technology selection, and cross-cutting concerns.

## Skills & Tools

### 1. Architectural Patterns
Selecting the right structure for the system.

- **Tool: Microservices vs. Monolith**
  - *Description*: Choosing between a single unit or distributed services.
  - *Practice*: Evaluate organizational structure (Conway's Law) and scalability needs.
  - *Agent Prompt*: "Compare Monolith vs. Microservices for a startup MVP."

- **Tool: Event-Driven Architecture**
  - *Description*: Using events to trigger and communicate between decoupled services.
  - *Practice*: Implement message brokers (Kafka, RabbitMQ).
  - *Agent Prompt*: "Design an event-driven flow for order processing."

- **Tool: Domain-Driven Design (DDD)**
  - *Description*: Aligning software structure with the business domain.
  - *Practice*: Define Bounded Contexts, Aggregates, and Entities.
  - *Agent Prompt*: "Identify Bounded Contexts for an E-commerce system."

### 2. System Design & Documentation
Communicating the architecture.

- **Tool: C4 Model**
  - *Description*: A standard for visualizing software architecture.
  - *Practice*: Create System Context, Container, and Component diagrams.
  - *Agent Prompt*: "Create a C4 Container diagram for the payment gateway integration."

- **Tool: Architecture Decision Records (ADR)**
  - *Description*: Documenting significant architectural decisions.
  - *Practice*: Record context, decision, consequences, and status.
  - *Agent Prompt*: "Write an ADR for adopting GraphQL over REST."

### 3. Quality Attributes (Non-Functional Requirements)
Ensuring the system meets quality standards.

- **Tool: Scalability Analysis**
  - *Description*: Ensuring the system can handle growth.
  - *Practice*: Design for horizontal scaling and load balancing.
  - *Agent Prompt*: "Design a strategy to scale the database for 10x traffic."

- **Tool: Reliability & Resilience Patterns**
  - *Description*: Handling failures gracefully.
  - *Practice*: Implement Circuit Breakers, Retries, and Bulkheads.
  - *Agent Prompt*: "Implement a Circuit Breaker pattern for the external API call."

### 4. Technology Selection
Choosing the right tools for the job.

- **Tool: Tech Radar**
  - *Description*: Visualizing the technology portfolio.
  - *Practice*: Assess technologies (Assess, Trial, Adopt, Hold).
  - *Agent Prompt*: "Create a Tech Radar entry for 'Rust' language."

- **Tool: Proof of Concept (POC)**
  - *Description*: Validating technical feasibility.
  - *Practice*: Build prototypes to test critical assumptions.
  - *Agent Prompt*: "Outline a POC to test the performance of ScyllaDB."
