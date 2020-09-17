Requires Changes
----------------

### 3 specifications require changes

Dear Student,

Thanks for your submission. You're inches away from completing this project. But don't worry.

Kindly go through the suggestions carefully and please take them positively and constructively as an opportunity to learn and grow and also improve the overall quality of your work.

Please take care to review each of the specifications to ensure that you are meeting all of the requirements before you submit your project again. You are very close for acceptance, and your submission requires minor changes before acceptance. Please don't take this in negative way, but a chance for learning and improving. Remember the passing of project might take time but it's not about how quickly you submit or even pass, it's about how much actually you learn from this project and this nanodegree in general.

Also If this review helped you in some way, Please consider rating it positively.\
I wish you the best, please don't give up and submit again with more zeal and enthusiasm.

ETL Pipeline Processing
-----------------------

Student creates `event_data_new.csv` file.

Nice job ! I see the event_data_new.csv file, which indicates you followed the ETL pipeline to create the csv file.

Student uses the appropriate datatype within the `CREATE` statement.

You use the appropriate datatypes. Be sure to keep this link handy for future Cassandra project when assigning the correct data types\
(<https://docs.datastax.com/en/cql/3.3/cql/cql_reference/cql_data_types_c.html>)

Data Modeling
-------------

Student creates the correct Apache Cassandra tables for each of the three queries. The `CREATE TABLE` statement should include the appropriate table.

Great job! You followed the one table per query rule of Apache Cassandra. You are not replicating the same table for all three queries, which defies that rule. You have three distinct tables with unique tables names and uses appropriate CREATE table statements.

Student demonstrates good understanding of data modeling by generating correct SELECT statements to generate the result being asked for in the question.

The SELECT statement should NOT use `ALLOW FILTERING` to generate the results.

Good job with 1 & 2.\
For Query 3: We need to Use SELECT to pick first and last names columns and printout that.

Currently you're not inserting that so not selecting as well.\
Please add these in insert and select.

Student should use table names that reflect the query and the result it will generate. Table names should include alphanumeric characters and underscores, and table names must start with a letter.

The sequence in which columns appear should reflect how the data is partitioned and the order of the data within the partitions.

There's a slight issue with query 2 where `item_in_session` inspite of being part of PRIMARY KEY is moved to the end while inserting.

The sequence of the columns in the CREATE and INSERT statements should follow the order of the COMPOSITE PRIMARY KEY and CLUSTERING columns. The data should be inserted and retrieved in the same order as how the COMPOSITE PRIMARY KEY is set up. This is important because Apache Cassandra is a partition row store, which means the partition key determines which any particular row is stored on which node. In case of composite partition key, partitions are distributed across the nodes of the cluster and how they are chunked for write purposes. Any clustering column(s) would determine the order in which the data is sorted within the partition.

PRIMARY KEYS
------------

The combination of the PARTITION KEY alone or with the addition of CLUSTERING COLUMNS should be used appropriately to uniquely identify each row.

Good job with Query 1 & Query 3

For Query 2 :\
You have used PRIMARY KEY(userId, sessionId, itemInSession). However, note that this is not an optimal choice of partition key (currently only userId) because sessions belonging to the same user might be in different nodes. This will cause a performance issue if the database is very large. Therefore we should use both userId and sessionId as partition keys so sessions from the same user are stored together. You can do this by PRIMARY KEY((userId, sessionId), itemInSession).

Presentation
------------

The notebooks should include a description of the query the data is modeled after.

Code should be organized well into the different queries. Any in-line comments that were clearly part of the project instructions should be removed so the notebook provides a professional look.

Nice work !\
Your notebook is well formatted. Another further improvement suggestion is that you can also add additional images and project overview to give more context about the project.