# Database Engineer Skills

The Database Engineer (DBA) is responsible for designing, implementing, maintaining, and optimizing databases.

## Role Definition
Focuses on data modeling, query optimization, backup/recovery, and database security.

## Skills & Tools

### 1. Database Design & Modeling
Structuring data efficiently.

- **Tool: ER Diagrams**
  - *Description*: Visualizing entities and relationships.
  - *Practice*: Normalization (1NF, 2NF, 3NF) to reduce redundancy.
  - *Agent Prompt*: "Design a normalized database schema for a library management system."

- **Tool: Schema Migration**
  - *Description*: Managing database changes over time (Flyway, Liquibase).
  - *Practice*: Version control database schemas.
  - *Agent Prompt*: "Create a Flyway migration script to add a 'status' column to the 'orders' table."

### 2. Query Optimization
Ensuring fast data retrieval.

- **Tool: Explain Plan**
  - *Description*: Analyzing how the database executes a query.
  - *Practice*: Identify full table scans and missing indexes.
  - *Agent Prompt*: "Analyze this SQL query using EXPLAIN ANALYZE and suggest indexes."

- **Tool: Indexing Strategies**
  - *Description*: B-Tree, Hash, GIN, GiST indexes.
  - *Practice*: Create appropriate indexes for common query patterns.
  - *Agent Prompt*: "Create a composite index for querying users by 'last_name' and 'city'."

### 3. Administration & Maintenance
Keeping the database healthy.

- **Tool: Backup & Recovery**
  - *Description*: Protecting against data loss.
  - *Practice*: Schedule full and incremental backups; test Point-in-Time Recovery (PITR).
  - *Agent Prompt*: "Draft a backup strategy for a mission-critical PostgreSQL database."

- **Tool: Replication & Clustering**
  - *Description*: High availability and read scaling.
  - *Practice*: Configure Master-Slave or Multi-Master replication.
  - *Agent Prompt*: "Explain how to set up PostgreSQL streaming replication."

### 4. NoSQL & Big Data
Handling unstructured or massive data.

- **Tool: Document Stores (MongoDB)**
  - *Description*: Storing data as JSON-like documents.
  - *Practice*: Design schemas for flexibility and aggregation.
  - *Agent Prompt*: "Design a MongoDB aggregation pipeline to calculate daily sales."

- **Tool: Key-Value Stores (Redis)**
  - *Description*: Fast in-memory storage.
  - *Practice*: Implement caching and session storage.
  - *Agent Prompt*: "Implement a Redis caching strategy for API responses."
