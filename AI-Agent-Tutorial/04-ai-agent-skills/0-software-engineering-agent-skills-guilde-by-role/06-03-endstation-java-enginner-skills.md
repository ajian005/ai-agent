# Java Engineer (Backend) Skills

The Java Engineer specializes in building robust, scalable backend systems using the Java ecosystem.

## Role Definition
Focuses on object-oriented design, JVM internals, Spring Framework, and enterprise patterns.

## Skills & Tools

### 1. Core Java & JVM
Mastering the language and runtime.

- **Tool: Java Stream API**
  - *Description*: Functional-style operations on streams of elements.
  - *Practice*: Process collections efficiently (filter, map, reduce).
  - *Agent Prompt*: "Refactor this loop to use Java Streams."

- **Tool: Concurrency**
  - *Description*: Multi-threading and parallel execution.
  - *Practice*: Use `CompletableFuture`, `ExecutorService`, and synchronization.
  - *Agent Prompt*: "Implement an asynchronous task using CompletableFuture."

- **Tool: JVM Tuning**
  - *Description*: Optimizing Java Virtual Machine performance.
  - *Practice*: Analyze Garbage Collection (GC) logs and adjust heap size.
  - *Agent Prompt*: "Suggest JVM flags to optimize for low latency."

### 2. Spring Ecosystem
Building enterprise applications.

- **Tool: Spring Boot**
  - *Description*: Framework for creating stand-alone, production-grade Spring apps.
  - *Practice*: Use starters, auto-configuration, and embedded servers.
  - *Agent Prompt*: "Create a Spring Boot application with a REST controller."

- **Tool: Spring Data JPA**
  - *Description*: Simplifying database access.
  - *Practice*: Define repositories and query methods.
  - *Agent Prompt*: "Create a JPA repository interface for the 'Product' entity."

- **Tool: Spring Security**
  - *Description*: Authentication and access control.
  - *Practice*: Configure JWT filters and role-based security.
  - *Agent Prompt*: "Configure Spring Security to require authentication for /api/** endpoints."

### 3. Microservices with Spring Cloud
Building distributed systems.

- **Tool: Service Discovery (Eureka/Consul)**
  - *Description*: Locating services dynamically.
  - *Practice*: Register and discover services.
  - *Agent Prompt*: "Configure a Eureka client in Spring Boot."

- **Tool: API Gateway (Spring Cloud Gateway)**
  - *Description*: Unified entry point for the system.
  - *Practice*: Route requests and handle cross-cutting concerns (rate limiting).
  - *Agent Prompt*: "Set up a route in Spring Cloud Gateway with a rate limiter."

### 4. Testing
Ensuring code quality.

- **Tool: JUnit 5**
  - *Description*: Standard unit testing framework.
  - *Practice*: Write parameterized tests and use assertions.
  - *Agent Prompt*: "Write a JUnit 5 test for the 'calculateTotal' method."

- **Tool: Mockito**
  - *Description*: Mocking framework for unit tests.
  - *Practice*: Mock dependencies to isolate the unit under test.
  - *Agent Prompt*: "Mock the 'UserRepository' to return a dummy user."
