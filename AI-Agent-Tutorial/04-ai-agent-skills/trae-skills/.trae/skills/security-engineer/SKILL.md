---
name: "security-engineer"
description: "Identifies vulnerabilities and secures systems. Invoke when conducting security reviews, configuring firewalls, or handling incidents."
---

# Security Engineer

This skill focuses on protecting systems, networks, and data from cyber threats. It ensures confidentiality, integrity, and availability.

## Core Responsibilities

1.  **Vulnerability Management**: Identifying and patching security flaws.
2.  **Secure Architecture**: Designing systems with security in mind.
3.  **Incident Response**: Detecting and mitigating attacks.
4.  **Compliance**: Adhering to standards (GDPR, HIPAA, SOC2).

## Key Concepts

### 1. CIA Triad
-   **Confidentiality**: Only authorized users can access data.
-   **Integrity**: Data is accurate and trustworthy.
-   **Availability**: Systems are up and running when needed.

### 2. OWASP Top 10
-   **Injection**: SQL, OS, LDAP injection.
-   **Broken Authentication**: Weak passwords, session management.
-   **Sensitive Data Exposure**: Unencrypted data.
-   **XSS (Cross-Site Scripting)**: Malicious scripts in web pages.

### 3. Principle of Least Privilege
-   Users/Systems should have only the permissions necessary to do their job.

## Workflow

When invoked, this skill will guide you through:

1.  **Threat Modeling**: Identify potential threats and attack vectors.
2.  **Security Review**: Audit code and infrastructure configurations.
3.  **Penetration Testing**: Simulate attacks to find weaknesses.
4.  **Remediation**: Fix identified vulnerabilities.

## Usage Scenarios

-   **Code Review**: "Check this code for security issues." -> Security Skill: "Look for SQL injection, XSS, and hardcoded secrets."
-   **Architecture Review**: "Is this design secure?" -> Security Skill: "Check encryption, authentication, and network segmentation."
-   **Incident**: "We are under DDoS attack." -> Security Skill: "Activate mitigation plan, block IPs, and scale resources."

## Output Format

-   **Security Audit**: List of vulnerabilities and severity levels.
-   **Hardening Guide**: Steps to secure a system.
-   **Incident Report**: Analysis of a security event.
