---
name: "python-code-standard"
description: "Enforces Python coding standards (PEP 8, type hints, docstrings). Invoke when writing, refactoring, or reviewing Python code."
---

# Python Code Standard

This skill ensures Python code adheres to best practices, readability, and maintainability standards.

## Core Principles

1.  **Readability Counts**: Code is read more often than it is written.
2.  **Explicit is Better than Implicit**: Avoid magic numbers, hidden dependencies, and overly complex one-liners.
3.  **Strict Typing**: Use type hints for all function signatures and complex variables.
4.  **Robust Error Handling**: Use specific exceptions and avoid bare `except:`.

## Coding Guidelines

### 1. Style & Formatting (PEP 8)
-   **Indentation**: Use 4 spaces per indentation level. No tabs.
-   **Line Length**: Limit lines to 79 characters (docstrings/comments to 72). extend to 100 or 120 only if readability improves significantly.
-   **Imports**:
    -   Group imports: Standard library -> Third-party -> Local application.
    -   Use absolute imports for clarity.
    -   Avoid `from module import *`.

### 2. Type Hinting
-   Annotate all function arguments and return values.
-   Use `typing.Optional`, `typing.List`, `typing.Dict`, etc., for complex types (or standard collection types in Python 3.9+).
-   Use `mypy` or similar tools for static type checking.

```python
def process_data(data: List[int]) -> Optional[float]:
    if not data:
        return None
    return sum(data) / len(data)
```

### 3. Documentation (Docstrings)
-   Use **Google Style** or **NumPy Style** docstrings.
-   Document all public modules, classes, and functions.
-   Include `Args`, `Returns`, and `Raises` sections.

```python
def fetch_user(user_id: int) -> User:
    """Fetches a user by ID.

    Args:
        user_id (int): The unique identifier of the user.

    Returns:
        User: The user object found.

    Raises:
        UserNotFoundError: If no user with the given ID exists.
    """
    ...
```

### 4. Naming Conventions
-   **Variables/Functions**: `snake_case`
-   **Classes/Exceptions**: `PascalCase`
-   **Constants**: `UPPER_CASE`
-   **Private Members**: `_leading_underscore`

### 5. Error Handling
-   Catch specific exceptions, not broad `Exception`.
-   Use `try/except/else/finally` blocks appropriately.
-   Log errors with context (stack trace, variable values).

### 6. Testing
-   Write unit tests using `pytest`.
-   Aim for high test coverage.
-   Test edge cases and error conditions.

## Usage

Invoke this skill whenever you are:
-   Writing new Python code.
-   Refactoring existing Python code.
-   Reviewing Python code for quality assurance.
-   Setting up a new Python project.
