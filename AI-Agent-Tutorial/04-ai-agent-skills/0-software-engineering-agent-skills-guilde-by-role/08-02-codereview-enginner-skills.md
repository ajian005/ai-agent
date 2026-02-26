# Code Review Engineer Skills

The Code Review Engineer (often a senior role) ensures code quality, security, and maintainability through rigorous peer review.

## Role Definition
Focuses on static analysis, style enforcement, architectural alignment, and mentorship.

## Skills & Tools

### 1. Static Analysis (SAST)
Automating code checks.

- **Tool: SonarQube**
  - *Description*: Continuous inspection of code quality.
  - *Practice*: Detect bugs, vulnerabilities, and code smells.
  - *Agent Prompt*: "Analyze the SonarQube report for the 'Payment' module."

- **Tool: ESLint / Pylint**
  - *Description*: Linters for JavaScript and Python.
  - *Practice*: Enforce coding standards and find syntax errors.
  - *Agent Prompt*: "Configure ESLint to disallow unused variables."

### 2. Code Review Process
Reviewing logic and design.

- **Tool: GitHub / GitLab Pull Requests**
  - *Description*: Platforms for code review.
  - *Practice*: Review diffs, leave comments, and request changes.
  - *Agent Prompt*: "Draft a code review comment suggesting a more efficient algorithm."

- **Tool: Review Checklist**
  - *Description*: Standardized criteria for approval.
  - *Practice*: Check for readability, test coverage, and security.
  - *Agent Prompt*: "Create a code review checklist for backend API changes."

### 3. Style & Formatting
Ensuring consistency.

- **Tool: Prettier / Black**
  - *Description*: Code formatters.
  - *Practice*: Automate formatting to avoid style debates.
  - *Agent Prompt*: "Set up Prettier to run on git commit using Husky."

- **Tool: Style Guides (Google/Airbnb)**
  - *Description*: Official style guides for languages.
  - *Practice*: Reference standards during reviews.
  - *Agent Prompt*: "Does this Java code follow the Google Java Style Guide?"

### 4. Mentorship
Teaching through review.

- **Tool: Constructive Feedback**
  - *Description*: Giving feedback that helps the author improve.
  - *Practice*: Focus on the code, not the person. Use "We" instead of "You".
  - *Agent Prompt*: "Rewrite this critical comment to be more constructive and helpful."

- **Tool: Documentation Links**
  - *Description*: Linking to docs or patterns.
  - *Practice*: Provide resources for learning.
  - *Agent Prompt*: "Find the official documentation for React Hooks to explain the issue."
