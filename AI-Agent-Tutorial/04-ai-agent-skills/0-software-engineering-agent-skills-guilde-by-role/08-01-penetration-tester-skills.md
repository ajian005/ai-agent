# Penetration Tester Skills

The Penetration Tester (Ethical Hacker) simulates cyberattacks to identify and fix security vulnerabilities before malicious hackers can exploit them.

## Role Definition
Focuses on vulnerability exploitation, network scanning, social engineering, and security reporting.

## Skills & Tools

### 1. Reconnaissance & Scanning
Gathering information about the target.

- **Tool: Nmap**
  - *Description*: Network discovery and security auditing.
  - *Practice*: Scan for open ports and running services.
  - *Agent Prompt*: "Run an Nmap scan to identify all open ports on the target IP."

- **Tool: OSINT (Open Source Intelligence)**
  - *Description*: Gathering data from public sources.
  - *Practice*: Use tools like Shodan or TheHarvester.
  - *Agent Prompt*: "Use Shodan to find exposed webcams in a specific region."

### 2. Vulnerability Assessment
Finding weaknesses.

- **Tool: Nessus / OpenVAS**
  - *Description*: Automated vulnerability scanners.
  - *Practice*: Configure and run scans against infrastructure.
  - *Agent Prompt*: "Analyze the Nessus report and filter for critical vulnerabilities."

- **Tool: Burp Suite**
  - *Description*: Web vulnerability scanner and proxy.
  - *Practice*: Intercept and modify web traffic to test for SQLi, XSS.
  - *Agent Prompt*: "Configure Burp Suite to intercept HTTPS traffic from the browser."

### 3. Exploitation
Proving the vulnerability exists.

- **Tool: Metasploit Framework**
  - *Description*: Exploitation tool for developing and executing exploit code.
  - *Practice*: Select payloads and launch attacks.
  - *Agent Prompt*: "Search for an exploit module for the specific Apache version."

- **Tool: SQLMap**
  - *Description*: Automated SQL injection tool.
  - *Practice*: Dump database tables via a vulnerable parameter.
  - *Agent Prompt*: "Use SQLMap to test the 'id' parameter for injection."

### 4. Reporting
Communicating findings.

- **Tool: Documentation**
  - *Description*: Writing clear, actionable reports.
  - *Practice*: Document the methodology, evidence (screenshots), and remediation.
  - *Agent Prompt*: "Draft a penetration test report summarizing the found RCE vulnerability."

- **Tool: CVSS Scoring**
  - *Description*: Common Vulnerability Scoring System.
  - *Practice*: Assign severity scores to findings.
  - *Agent Prompt*: "Calculate the CVSS score for a reflected XSS vulnerability."
