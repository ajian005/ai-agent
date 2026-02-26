# C++ Engineer Skills

The C++ Engineer builds high-performance applications, often working close to the hardware, in gaming, finance, or embedded systems.

## Role Definition
Focuses on memory management, performance optimization, system-level programming, and modern C++ standards.

## Skills & Tools

### 1. Modern C++
Using the latest standards (C++11/14/17/20/23).

- **Tool: Smart Pointers**
  - *Description*: `std::unique_ptr`, `std::shared_ptr`.
  - *Practice*: Manage resource lifecycles without manual `new`/`delete`.
  - *Agent Prompt*: "Refactor this raw pointer code to use `std::unique_ptr`."

- **Tool: Move Semantics**
  - *Description*: Transferring resources instead of copying.
  - *Practice*: Optimize performance using rvalue references.
  - *Agent Prompt*: "Implement a move constructor for this custom string class."

- **Tool: STL (Standard Template Library)**
  - *Description*: Algorithms and data structures.
  - *Practice*: Use vectors, maps, and algorithms effectively.
  - *Agent Prompt*: "Use `std::sort` with a custom lambda comparator."

### 2. Build Systems & Package Management
Managing the build process.

- **Tool: CMake**
  - *Description*: Cross-platform build system generator.
  - *Practice*: Define targets, libraries, and dependencies.
  - *Agent Prompt*: "Write a `CMakeLists.txt` to build a project with two executables."

- **Tool: Conan / Vcpkg**
  - *Description*: C++ package managers.
  - *Practice*: Manage third-party libraries.
  - *Agent Prompt*: "Create a `conanfile.txt` to install Boost and GTest."

### 3. Debugging & Profiling
Fixing and optimizing code.

- **Tool: GDB / LLDB**
  - *Description*: Command-line debuggers.
  - *Practice*: Inspect stack traces, variables, and memory.
  - *Agent Prompt*: "Explain how to set a breakpoint and inspect a variable in GDB."

- **Tool: Valgrind / Sanitizers**
  - *Description*: Memory error detectors.
  - *Practice*: Detect memory leaks and buffer overflows.
  - *Agent Prompt*: "Run the program with AddressSanitizer to check for out-of-bounds access."

### 4. Concurrency
Writing multi-threaded code.

- **Tool: `std::thread` / `std::async`**
  - *Description*: C++ concurrency support.
  - *Practice*: Avoid race conditions using mutexes and locks.
  - *Agent Prompt*: "Implement a thread-safe queue using `std::mutex` and `std::condition_variable`."
