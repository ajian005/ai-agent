---
name: "unit-test-engineer"
description: "Writes granular tests for code components. Invoke when ensuring code coverage, mocking dependencies, or practicing TDD."
---

# Unit Test Engineer

This skill focuses on verifying the correctness of individual units of code (functions, classes) in isolation.

## Core Responsibilities

1.  **Test Creation**: Writing test cases for various scenarios (happy path, edge cases).
2.  **Mocking**: Isolating the unit by simulating dependencies.
3.  **Coverage**: Ensuring a high percentage of code is executed during tests.
4.  **TDD**: Writing tests before the implementation.

## Key Concepts

### 1. AAA Pattern
-   **Arrange**: Set up the test data and mocks.
-   **Act**: Call the method under test.
-   **Assert**: Verify the result matches expectations.

### 2. Mocking vs. Stubbing
-   **Mock**: Verifying interactions (e.g., "was `save()` called?").
-   **Stub**: Providing canned answers (e.g., "return 42 when `getCount()` is called").

## Workflow

When invoked, this skill will guide you through:

1.  **Analysis**: Understand the function's logic and branches.
2.  **Scenarios**: Identify valid inputs, invalid inputs, and boundary conditions.
3.  **Implementation**: Write the test code using a framework (Jest, Pytest, JUnit).
4.  **Refinement**: Improve coverage and assertion clarity.

## Usage Scenarios

-   **New Function**: "Test this email validator." -> Unit Test Skill: "Test 'user@example.com', 'invalid-email', and empty string."
-   **Bug Fix**: "Prevent this crash." -> Unit Test Skill: "Write a test case that reproduces the crash, then fix the code."
-   **Refactoring**: "Ensure I didn't break anything." -> Unit Test Skill: "Run the existing test suite and check for regressions."

## Output Format

-   **Test File**: Complete test suite code.
-   **Coverage Report**: Analysis of tested lines.
-   **Mock Setup**: Code for configuring mocks.
