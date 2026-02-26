# Data Engineer Skills

The Data Engineer builds the infrastructure and pipelines that allow data to be collected, stored, processed, and analyzed. They are the "plumbers" of the data world.

## Role Definition
Focuses on ETL/ELT pipelines, data warehousing, data quality, and big data processing.

## Skills & Tools

### 1. Data Pipelines (ETL/ELT)
Moving and transforming data.

- **Tool: Apache Airflow**
  - *Description*: Workflow orchestration management.
  - *Practice*: Schedule and monitor complex data workflows (DAGs).
  - *Agent Prompt*: "Create an Airflow DAG to ingest data from an API to S3 daily."

- **Tool: dbt (data build tool)**
  - *Description*: Transformation tool that runs inside the warehouse.
  - *Practice*: Write SQL to transform data and manage dependencies.
  - *Agent Prompt*: "Create a dbt model to aggregate daily sales from raw transactions."

### 2. Big Data Processing
Handling massive datasets.

- **Tool: Apache Spark**
  - *Description*: Unified analytics engine for large-scale data processing.
  - *Practice*: Write PySpark jobs for batch and streaming data.
  - *Agent Prompt*: "Write a PySpark script to filter and aggregate 1TB of logs."

- **Tool: Kafka**
  - *Description*: Distributed event streaming platform.
  - *Practice*: Build real-time data pipelines.
  - *Agent Prompt*: "Configure a Kafka Connect source connector for PostgreSQL."

### 3. Data Warehousing & Lakes
Storing data for analysis.

- **Tool: Snowflake / BigQuery / Redshift**
  - *Description*: Cloud data warehouses.
  - *Practice*: Optimize table structures, clustering, and partitioning.
  - *Agent Prompt*: "Optimize a Snowflake table for queries filtering by 'timestamp'."

- **Tool: Data Lakes (S3 / HDFS)**
  - *Description*: Storage for raw, unstructured data.
  - *Practice*: Organize data using Hive partitioning (e.g., year/month/day).
  - *Agent Prompt*: "Design a directory structure for a data lake on S3."

### 4. Data Quality & Governance
Ensuring data is reliable.

- **Tool: Great Expectations**
  - *Description*: Tool for validating, documenting, and profiling data.
  - *Practice*: Define assertions (e.g., "column X should not be null").
  - *Agent Prompt*: "Define a Great Expectations suite to validate customer email formats."

- **Tool: Data Catalog**
  - *Description*: Documentation of data assets (Amundsen, DataHub).
  - *Practice*: Maintain metadata and lineage.
  - *Agent Prompt*: "Describe how to capture data lineage in a complex pipeline."
