# Network Engineer Skills

The Network Engineer designs, implements, and maintains the networking infrastructure, ensuring connectivity, performance, and security.

## Role Definition
Focuses on routing, switching, firewalls, load balancing, and cloud networking.

## Skills & Tools

### 1. Network Fundamentals
Understanding how data moves.

- **Tool: TCP/IP Stack**
  - *Description*: The core protocols of the internet.
  - *Practice*: Subnetting, CIDR, DNS, HTTP/HTTPS.
  - *Agent Prompt*: "Calculate the subnet mask for a /28 network."

- **Tool: Wireshark**
  - *Description*: Network protocol analyzer.
  - *Practice*: Capture and inspect packets to troubleshoot issues.
  - *Agent Prompt*: "Analyze a Wireshark capture to identify a TCP retransmission issue."

### 2. Cloud Networking
Networking in the cloud (AWS/Azure/GCP).

- **Tool: VPC (Virtual Private Cloud)**
  - *Description*: Isolated cloud network environments.
  - *Practice*: Design subnets, route tables, and internet gateways.
  - *Agent Prompt*: "Design a VPC with public and private subnets across two availability zones."

- **Tool: Load Balancers**
  - *Description*: Distributing traffic (ALB/NLB).
  - *Practice*: Configure listeners, target groups, and health checks.
  - *Agent Prompt*: "Configure an Application Load Balancer for path-based routing."

### 3. Network Security
Securing the perimeter and internal traffic.

- **Tool: Firewalls / Security Groups**
  - *Description*: Controlling traffic flow.
  - *Practice*: Define ingress/egress rules based on least privilege.
  - *Agent Prompt*: "Audit AWS Security Groups for overly permissive rules."

- **Tool: VPN / Direct Connect**
  - *Description*: Connecting sites securely.
  - *Practice*: Set up Site-to-Site VPNs or dedicated connections.
  - *Agent Prompt*: "Explain the difference between a Client VPN and a Site-to-Site VPN."

### 4. Routing & Switching
Managing traffic flow.

- **Tool: BGP (Border Gateway Protocol)**
  - *Description*: The routing protocol of the internet.
  - *Practice*: Manage dynamic routing between networks.
  - *Agent Prompt*: "Explain how BGP path selection works."

- **Tool: Software Defined Networking (SDN)**
  - *Description*: Managing network programmatically.
  - *Practice*: Use overlay networks (e.g., Calico in Kubernetes).
  - *Agent Prompt*: "Describe how Calico manages networking in a Kubernetes cluster."
