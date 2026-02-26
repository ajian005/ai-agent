# Security Engineer Skills

The Security Engineer is responsible for protecting the organization's systems, networks, and data from cyber threats.

## Role Definition
Focuses on vulnerability assessment, secure coding, incident response, and compliance.

## Skills & Tools

### 1. Vulnerability Assessment & Penetration Testing
Identifying weaknesses in the system.

- **Tool: Vulnerability Scanners**
  - *Description*: Automated tools to find known vulnerabilities (Nessus, OpenVAS).
  - *Practice*: Regularly scan networks and applications.
  - *Agent Prompt*: "Interpret the Nessus scan report and prioritize fixes."

- **Tool: SAST / DAST**
  - *Description*: Static Application Security Testing (SonarQube) and Dynamic Application Security Testing (OWASP ZAP).
  - *Practice*: Integrate security testing into the CI/CD pipeline.
  - *Agent Prompt*: "Configure SonarQube to scan for SQL Injection vulnerabilities."

- **Tool: Penetration Testing**
  - *Description*: Simulating attacks to find security flaws (Metasploit, Burp Suite).
  - *Practice*: Test the system's defenses manually.
  - *Agent Prompt*: "Describe the steps to test for Cross-Site Scripting (XSS) using Burp Suite."

### 2. Application Security
Securing the software development lifecycle.

- **Tool: OWASP Top 10**
  - *Description*: A standard awareness document for developers and web application security.
  - *Practice*: Mitigate common risks like Injection, Broken Authentication, XSS.
  - *Agent Prompt*: "Review the code for OWASP Top 10 vulnerabilities."

- **Tool: Secure Coding Standards**
  - *Description*: Guidelines for writing secure code (CERT, CWE).
  - *Practice*: Enforce secure coding practices.
  - *Agent Prompt*: "Refactor this input validation logic to prevent buffer overflows."

### 3. Network & Infrastructure Security
Securing the network and servers.

- **Tool: Firewalls & IDS/IPS**
  - *Description*: Network security systems (iptables, Snort).
  - *Practice*: Filter traffic and detect intrusions.
  - *Agent Prompt*: "Configure firewall rules to allow only HTTPS traffic."

- **Tool: IAM (Identity and Access Management)**
  - *Description*: Managing user identities and permissions (AWS IAM, Active Directory).
  - *Practice*: Enforce Principle of Least Privilege.
  - *Agent Prompt*: "Audit AWS IAM roles for overly permissive policies."

### 4. Incident Response & Forensics
Handling security breaches.

- **Tool: SIEM (Security Information and Event Management)**
  - *Description*: Aggregating and analyzing security data (Splunk, ELK).
  - *Practice*: Detect and respond to security incidents.
  - *Agent Prompt*: "Create a SIEM alert for multiple failed login attempts."

- **Tool: Digital Forensics**
  - *Description*: Investigating cybercrimes.
  - *Practice*: Analyze logs and artifacts to determine the scope of a breach.
  - *Agent Prompt*: "Analyze the access logs to trace the attacker's IP address."
