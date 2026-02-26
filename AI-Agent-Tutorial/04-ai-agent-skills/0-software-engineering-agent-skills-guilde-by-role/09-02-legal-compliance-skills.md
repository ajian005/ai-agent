# Legal Compliance Skills

The Legal Compliance specialist (often working with Engineering) ensures software and business practices adhere to laws, regulations, and licenses.

## Role Definition
Focuses on OSS license compliance, export controls, accessibility laws, and industry standards.

## Skills & Tools

### 1. Open Source License Compliance
Managing third-party code risks.

- **Tool: FOSSA / Black Duck**
  - *Description*: Software Composition Analysis (SCA) tools.
  - *Practice*: Scan dependencies for license violations (e.g., GPL in proprietary code).
  - *Agent Prompt*: "Run a FOSSA scan and identify any GPL-3.0 dependencies."

- **Tool: SPDX (Software Package Data Exchange)**
  - *Description*: Standard for communicating software bill of materials (SBOM).
  - *Practice*: Generate SBOMs for releases.
  - *Agent Prompt*: "Generate an SBOM for the release in SPDX format."

### 2. Regulatory Compliance
Adhering to industry standards.

- **Tool: SOC 2 / ISO 27001**
  - *Description*: Security and compliance frameworks.
  - *Practice*: Implement controls and prepare for audits.
  - *Agent Prompt*: "List the key controls required for SOC 2 Type II compliance."

- **Tool: HIPAA / PCI-DSS**
  - *Description*: Health and Payment compliance standards.
  - *Practice*: Ensure systems handle PHI and credit card data correctly.
  - *Agent Prompt*: "Check if the log storage is compliant with PCI-DSS requirements."

### 3. Export Control
Managing international software distribution.

- **Tool: Encryption Export Controls**
  - *Description*: Regulations on exporting cryptographic software.
  - *Practice*: Classify software ECCN (Export Control Classification Number).
  - *Agent Prompt*: "Determine the ECCN for a mass-market app using standard HTTPS."

- **Tool: Sanctions Screening**
  - *Description*: Ensuring no business with sanctioned entities.
  - *Practice*: Screen user databases against OFAC lists.
  - *Agent Prompt*: "Explain the process for screening new customers against OFAC lists."

### 4. Audit & Governance
Verifying compliance.

- **Tool: Audit Logs**
  - *Description*: Immutable records of system activity.
  - *Practice*: Ensure critical actions are logged and retained.
  - *Agent Prompt*: "Define the retention policy for audit logs based on GDPR."

- **Tool: GRC Platforms**
  - *Description*: Governance, Risk, and Compliance software (Vanta, Drata).
  - *Practice*: Automate evidence collection for audits.
  - *Agent Prompt*: "Set up Vanta to monitor AWS infrastructure compliance."
