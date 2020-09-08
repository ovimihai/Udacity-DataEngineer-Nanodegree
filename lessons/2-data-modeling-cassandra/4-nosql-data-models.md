# NoSQL Data Models

### Not only SQL

When to use NoSQL databases:
- Need High Availability
- Have a Large Amounts of Data
- Need Linear Scalability
- Need Low Latency
- Need fast reads and writes

### CAP Theorem

- **Consistency**: Every read from the database gets the latest (and correct) piece of data or an error
- **Availability**: Every request is received and a response is given -- without a guarantee that the data is the latest update
- **Partition Tolerance**: The system continues to work regardless of losing network connectivity between nodes

### Data Modeling in Apache Cassandra:
- Denormalization is not just okay -- it's a must
- Denormalization must be done for fast reads
- Apache Cassandra has been optimized for fast writes
- **ALWAYS think Queries first**
- **One table per query** is a great strategy
- Apache Cassandra does **not** allow for JOINs between tables

### Primary Key

-   Must be unique
-   The PRIMARY KEY is made up of either just the PARTITION KEY or may also include additional CLUSTERING COLUMNS
-   A Simple PRIMARY KEY is just one column that is also the PARTITION KEY. A Composite PRIMARY KEY is made up of more than one column and will assist in creating a unique value and in your retrieval queries
-   The PARTITION KEY will determine the distribution of data across the system