# Mobile iOS Engineer Skills

The iOS Engineer specializes in building applications for Apple's ecosystem (iPhone, iPad, Watch, TV) using Swift and Objective-C.

## Role Definition
Focuses on UI/UX integration with UIKit/SwiftUI, performance tuning, and leveraging iOS SDKs.

## Skills & Tools

### 1. iOS Development
Building the app.

- **Tool: Swift**
  - *Description*: Apple's powerful and intuitive programming language.
  - *Practice*: Use optionals, closures, and protocol-oriented programming.
  - *Agent Prompt*: "Refactor this function to use Swift's `Result` type for error handling."

- **Tool: SwiftUI**
  - *Description*: Declarative framework for building user interfaces.
  - *Practice*: Build responsive layouts using Stacks and State.
  - *Agent Prompt*: "Create a SwiftUI view for a scrollable list of products."

- **Tool: UIKit**
  - *Description*: The traditional framework for managing graphical, event-driven user interfaces.
  - *Practice*: Manage ViewControllers and Auto Layout constraints.
  - *Agent Prompt*: "Programmatically create a `UITableView` with custom cells."

### 2. Architecture & Patterns
Structuring the code.

- **Tool: MVVM (Model-View-ViewModel)**
  - *Description*: Standard architectural pattern for iOS.
  - *Practice*: Separate logic from UI code.
  - *Agent Prompt*: "Design a ViewModel for the User Profile screen."

- **Tool: Combine / Swift Concurrency**
  - *Description*: Handling asynchronous events.
  - *Practice*: Use Publishers/Subscribers or async/await.
  - *Agent Prompt*: "Fetch data from an API using Swift's `async/await`."

### 3. Data & Networking
Handling data.

- **Tool: Core Data / SwiftData**
  - *Description*: Frameworks to manage the model layer objects in your application.
  - *Practice*: Persist user data locally.
  - *Agent Prompt*: "Create a Core Data entity for 'Task' with 'title' and 'dueDate'."

- **Tool: URLSession**
  - *Description*: Coordinating network data transfer tasks.
  - *Practice*: Perform API requests and handle JSON decoding.
  - *Agent Prompt*: "Write a network manager class to handle GET and POST requests."

### 4. Tooling & Distribution
Releasing the app.

- **Tool: Xcode**
  - *Description*: Apple's integrated development environment.
  - *Practice*: Debugging, profiling with Instruments.
  - *Agent Prompt*: "Explain how to use the Xcode Memory Graph Debugger to find retain cycles."

- **Tool: TestFlight / App Store Connect**
  - *Description*: Platforms for beta testing and release.
  - *Practice*: Manage provisioning profiles and certificates.
  - *Agent Prompt*: "Describe the steps to upload a build to TestFlight."
