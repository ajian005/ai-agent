# Privacy Engineer Skills

The Privacy Engineer ensures that systems are designed to protect user data and comply with privacy regulations (GDPR, CCPA).

## Role Definition
Focuses on data minimization, anonymization, privacy by design, and compliance auditing.

## Skills & Tools

### 1. Data Protection Techniques
Securing sensitive data.

- **Tool: Anonymization / Pseudonymization**
  - *Description*: Removing or masking PII (Personally Identifiable Information).
  - *Practice*: Implement k-anonymity or differential privacy.
  - *Agent Prompt*: "Explain the difference between anonymization and pseudonymization."

- **Tool: Encryption**
  - *Description*: Protecting data at rest and in transit.
  - *Practice*: Use AES-256 and TLS 1.3.
  - *Agent Prompt*: "Design an encryption strategy for storing user health records."

### 2. Privacy Compliance
Adhering to laws.

- **Tool: ROPA (Record of Processing Activities)**
  - *Description*: Documenting how data is processed.
  - *Practice*: Map data flows and legal basis for processing.
  - *Agent Prompt*: "Create a ROPA entry for the marketing email service."

- **Tool: DSAR (Data Subject Access Request)**
  - *Description*: Handling user requests to access or delete data.
  - *Practice*: Automate the retrieval and deletion of user data.
  - *Agent Prompt*: "Design a workflow to handle GDPR 'Right to be Forgotten' requests."

### 3. Privacy by Design
Embedding privacy into architecture.

- **Tool: PIA (Privacy Impact Assessment)**
  - *Description*: Evaluating risks of new projects.
  - *Practice*: Identify privacy risks early in the design phase.
  - *Agent Prompt*: "Conduct a PIA for the new facial recognition feature."

- **Tool: Data Minimization**
  - *Description*: Collecting only what is necessary.
  - *Practice*: Review data collection policies.
  - *Agent Prompt*: "Review the signup form and suggest fields to remove for data minimization."

### 4. Consent Management
Managing user permissions.

- **Tool: CMP (Consent Management Platform)**
  - *Description*: Tools like OneTrust or Cookiebot.
  - *Practice*: Manage cookie banners and user preferences.
  - *Agent Prompt*: "Configure OneTrust to block tracking scripts until consent is given."

- **Tool: Policy Management**
  - *Description*: Writing and updating privacy policies.
  - *Practice*: Ensure policies are clear and accurate.
  - *Agent Prompt*: "Draft a privacy policy update for the new mobile app."
