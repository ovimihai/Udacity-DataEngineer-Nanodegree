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

### Clustering Columns:

-   The clustering column will sort the data in sorted ascending order, e.g., alphabetical order. Note: this is a mistake in the video, which says descending order.
-   More than one clustering column can be added (or none!)
-   From there the clustering columns will sort in order of how they were added to the primary key

### WHERE clause

-   Data Modeling in Apache Cassandra is query focused, and that focus needs to be on the WHERE clause
-   Failure to include a WHERE clause will result in an error
- AVOID using "ALLOW FILTERING": Here is a reference [in DataStax](https://www.datastax.com/dev/blog/allow-filtering-explained-2) that explains ALLOW FILTERING and why you should not use it.


