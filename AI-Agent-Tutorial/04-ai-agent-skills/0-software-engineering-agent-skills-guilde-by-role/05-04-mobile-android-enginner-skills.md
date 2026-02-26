# Mobile Android Engineer Skills

The Android Engineer specializes in building applications for the Android operating system using Kotlin and Java.

## Role Definition
Focuses on Material Design, Android SDK, lifecycle management, and fragmentation handling.

## Skills & Tools

### 1. Android Development
Building the app.

- **Tool: Kotlin**
  - *Description*: The preferred language for Android development.
  - *Practice*: Use Coroutines, Null Safety, and Extension Functions.
  - *Agent Prompt*: "Rewrite this Java class in Kotlin using data classes."

- **Tool: Jetpack Compose**
  - *Description*: Android's modern toolkit for building native UI.
  - *Practice*: Build declarative UIs with less code.
  - *Agent Prompt*: "Create a Compose function for a reusable TopAppBar."

- **Tool: XML Layouts (Legacy)**
  - *Description*: Traditional way of defining UI.
  - *Practice*: Use ConstraintLayout for complex screens.
  - *Agent Prompt*: "Convert this nested LinearLayout to a ConstraintLayout."

### 2. Architecture & Jetpack Libraries
Structuring the code.

- **Tool: Android Architecture Components**
  - *Description*: Libraries for robust app architecture (ViewModel, LiveData, Lifecycle).
  - *Practice*: Handle configuration changes and lifecycle events.
  - *Agent Prompt*: "Implement a ViewModel to hold UI state across screen rotations."

- **Tool: Navigation Component**
  - *Description*: Managing app navigation.
  - *Practice*: Define navigation graphs and fragments.
  - *Agent Prompt*: "Set up a navigation graph with safe args."

### 3. Data & Networking
Handling data.

- **Tool: Room**
  - *Description*: Persistence library providing an abstraction layer over SQLite.
  - *Practice*: Cache data locally for offline use.
  - *Agent Prompt*: "Define a Room DAO for inserting and querying user logs."

- **Tool: Retrofit**
  - *Description*: Type-safe HTTP client for Android.
  - *Practice*: Define API interfaces and handle responses.
  - *Agent Prompt*: "Create a Retrofit service interface for the GitHub API."

### 4. Tooling & Performance
Releasing the app.

- **Tool: Android Studio**
  - *Description*: The official IDE for Android.
  - *Practice*: Use Logcat, Layout Inspector, and Profiler.
  - *Agent Prompt*: "How do I use the Network Profiler to inspect API calls?"

- **Tool: Gradle**
  - *Description*: Build automation tool.
  - *Practice*: Manage dependencies and build variants (Debug/Release).
  - *Agent Prompt*: "Configure the `build.gradle` file to add a new dependency."
