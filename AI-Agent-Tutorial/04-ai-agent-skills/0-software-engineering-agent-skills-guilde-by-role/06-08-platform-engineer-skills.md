# Platform Engineer Skills

The Platform Engineer builds the "Internal Developer Platform" (IDP) that enables product teams to ship software autonomously. They treat infrastructure as a product.

## Role Definition
Focuses on self-service tooling, standardizing infrastructure, developer experience (DevEx), and abstracting complexity.

## Skills & Tools

### 1. Internal Developer Platform (IDP)
Building the golden path.

- **Tool: Backstage**
  - *Description*: An open platform for building developer portals.
  - *Practice*: Centralize documentation, service catalog, and templates.
  - *Agent Prompt*: "Create a Backstage template for scaffolding a new Spring Boot service."

- **Tool: Service Catalog**
  - *Description*: A registry of all microservices and their ownership.
  - *Practice*: Track ownership, lifecycle, and dependencies.
  - *Agent Prompt*: "Define the metadata schema for services in the catalog."

### 2. Infrastructure Orchestration
Managing the underlying platform.

- **Tool: Kubernetes (Advanced)**
  - *Description*: Customizing K8s for the organization.
  - *Practice*: Write Custom Resource Definitions (CRDs) and Operators.
  - *Agent Prompt*: "Design a CRD for provisioning a 'Database' resource."

- **Tool: Crossplane / Terraform Cloud**
  - *Description*: Managing cloud infrastructure as code.
  - *Practice*: Provide high-level abstractions for developers.
  - *Agent Prompt*: "Create a Crossplane Composition to provision an AWS RDS instance."

### 3. Observability Platform
Providing monitoring as a service.

- **Tool: Centralized Logging/Metrics**
  - *Description*: Managing the stack (Prometheus/Grafana/ELK) for everyone.
  - *Practice*: Provide standard dashboards and alert rules.
  - *Agent Prompt*: "Create a default Grafana dashboard template for Go services."

- **Tool: OpenTelemetry**
  - *Description*: Observability framework.
  - *Practice*: Standardize tracing and metrics collection.
  - *Agent Prompt*: "Configure the OpenTelemetry Collector to forward traces to Jaeger."

### 4. Developer Experience (DevEx)
Reducing friction.

- **Tool: CLI Tools**
  - *Description*: Custom command-line interfaces for developers.
  - *Practice*: Automate common tasks (e.g., `company-cli deploy`).
  - *Agent Prompt*: "Design a CLI command to generate a new microservice from a template."

- **Tool: Documentation**
  - *Description*: Clear guides and "Golden Paths".
  - *Practice*: Write tutorials for the supported tech stack.
  - *Agent Prompt*: "Draft a 'Getting Started' guide for deploying a service to the platform."
