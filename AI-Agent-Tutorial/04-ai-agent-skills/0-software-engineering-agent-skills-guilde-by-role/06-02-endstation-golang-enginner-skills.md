# Golang Engineer Skills

The Golang (Go) Engineer builds scalable, concurrent, and efficient backend services, often for cloud-native environments.

## Role Definition
Focuses on simplicity, concurrency (goroutines), microservices, and high-throughput systems.

## Skills & Tools

### 1. Core Go
Mastering the language.

- **Tool: Goroutines & Channels**
  - *Description*: Lightweight threads and communication primitives.
  - *Practice*: Implement concurrent patterns (Worker Pool, Fan-out/Fan-in).
  - *Agent Prompt*: "Implement a worker pool pattern to process jobs concurrently."

- **Tool: Interfaces**
  - *Description*: Defining behavior contracts.
  - *Practice*: Write decoupled and testable code.
  - *Agent Prompt*: "Refactor this struct to satisfy the `io.Reader` interface."

- **Tool: Error Handling**
  - *Description*: Explicit error checking.
  - *Practice*: Handle errors idiomatically (`if err != nil`).
  - *Agent Prompt*: "Wrap an error with context using `fmt.Errorf`."

### 2. Web Development
Building APIs and services.

- **Tool: Gin / Echo / Standard Library**
  - *Description*: Web frameworks and HTTP packages.
  - *Practice*: Build RESTful APIs with middleware.
  - *Agent Prompt*: "Create a Gin server with a middleware for logging requests."

- **Tool: gRPC**
  - *Description*: High-performance RPC framework.
  - *Practice*: Define Protocol Buffers and generate Go code.
  - *Agent Prompt*: "Define a .proto file for a User Service and implement the server in Go."

### 3. Tooling & Ecosystem
Using the Go toolchain.

- **Tool: Go Modules**
  - *Description*: Dependency management.
  - *Practice*: Manage `go.mod` and `go.sum`.
  - *Agent Prompt*: "Initialize a new Go module and add `zap` logger as a dependency."

- **Tool: pprof**
  - *Description*: Profiling tool.
  - *Practice*: Analyze CPU and memory usage.
  - *Agent Prompt*: "Explain how to capture a heap profile from a running Go service."

### 4. Testing
Ensuring reliability.

- **Tool: `testing` package**
  - *Description*: Built-in testing support.
  - *Practice*: Write unit tests and table-driven tests.
  - *Agent Prompt*: "Write a table-driven test for an `Add` function."

- **Tool: `testify`**
  - *Description*: Assertion and mocking library.
  - *Practice*: Use assertions for more readable tests.
  - *Agent Prompt*: "Use `testify/assert` to verify the JSON response."
