# Unit Test Engineer Skills

The Unit Test Engineer (often part of the Developer role) specializes in writing granular tests for individual components or functions to ensure they work in isolation.

## Role Definition
Focuses on code coverage, mocking dependencies, edge cases, and test-driven development (TDD).

## Skills & Tools

### 1. Test Frameworks
Writing and running tests.

- **Tool: xUnit (JUnit, Pytest, Jest)**
  - *Description*: Standard testing frameworks for various languages.
  - *Practice*: Structure tests with Setup, Exercise, Verify, Teardown.
  - *Agent Prompt*: "Write a Pytest function to test the `calculate_tax` method."

- **Tool: Assertions**
  - *Description*: Verifying expected outcomes.
  - *Practice*: Use libraries like Chai, AssertJ, or built-in assertions.
  - *Agent Prompt*: "Write assertions to verify that the returned list is not empty and contains specific values."

### 2. Mocking & Stubbing
Isolating the unit under test.

- **Tool: Mocking Libraries**
  - *Description*: Mockito, unittest.mock, Jest Mocks.
  - *Practice*: Replace external dependencies (DB, API) with mock objects.
  - *Agent Prompt*: "Mock the database call in this service method using Mockito."

- **Tool: Dependency Injection**
  - *Description*: Design pattern to facilitate testing.
  - *Practice*: Inject dependencies to allow easy swapping with mocks.
  - *Agent Prompt*: "Refactor this class to use constructor injection for better testability."

### 3. Test Coverage
Measuring test effectiveness.

- **Tool: Coverage Tools**
  - *Description*: JaCoCo, coverage.py, Istanbul.
  - *Practice*: Analyze reports to identify untested code paths.
  - *Agent Prompt*: "Generate a coverage report for the `auth` module and identify missing branches."

- **Tool: Mutation Testing**
  - *Description*: Pitest, Stryker.
  - *Practice*: Modify code to ensure tests fail (verifying test quality).
  - *Agent Prompt*: "Run mutation testing on the core calculation logic."

### 4. Test Design Techniques
Writing effective tests.

- **Tool: Boundary Value Analysis**
  - *Description*: Testing at the edges of input ranges.
  - *Practice*: Test minimum, maximum, and just outside boundaries.
  - *Agent Prompt*: "Design test cases for an input field that accepts values 1-100."

- **Tool: Equivalence Partitioning**
  - *Description*: Grouping inputs that should be treated similarly.
  - *Practice*: Reduce the number of test cases while maintaining coverage.
  - *Agent Prompt*: "Identify equivalence classes for a credit score validator."
