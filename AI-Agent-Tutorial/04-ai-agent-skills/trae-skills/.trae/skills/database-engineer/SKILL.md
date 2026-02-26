---
name: "database-engineer"
description: "Designs and optimizes databases. Invoke when creating schemas, writing complex queries, or tuning performance."
---

# Database Engineer (DBA)

This skill focuses on the storage, retrieval, and management of data. It ensures data integrity, performance, and availability.

## Core Responsibilities

1.  **Schema Design**: Modeling data for efficiency and clarity.
2.  **Query Optimization**: Writing and tuning SQL for speed.
3.  **Maintenance**: Backups, migrations, and indexing.
4.  **Selection**: Choosing the right DB (Relational, Document, Key-Value).

## Key Concepts

### 1. Normalization
-   Organizing data to reduce redundancy (1NF, 2NF, 3NF).

### 2. ACID Properties
-   **Atomicity, Consistency, Isolation, Durability**: Ensuring reliable transactions.

### 3. Indexing
-   Creating data structures to speed up retrieval.

## Workflow

When invoked, this skill will guide you through:

1.  **Requirement**: Understand the data and access patterns.
2.  **Modeling**: Create an ERD (Entity Relationship Diagram).
3.  **Implementation**: Write DDL (Data Definition Language) to create tables.
4.  **Optimization**: Analyze query plans and add indexes.

## Usage Scenarios

-   **New App**: "Design the DB for a chat app." -> DB Skill: "Use PostgreSQL for users and Cassandra/MongoDB for message history."
-   **Slow Query**: "This report takes forever." -> DB Skill: "Run `EXPLAIN ANALYZE`, add a composite index, and rewrite the JOIN."
-   **Migration**: "Add a column without downtime." -> DB Skill: "Use a migration tool to add the column as nullable first."

## Output Format

-   **SQL Script**: CREATE TABLE / ALTER TABLE statements.
-   **ER Diagram**: Visual schema representation.
-   **Optimization Report**: Analysis of query performance.
