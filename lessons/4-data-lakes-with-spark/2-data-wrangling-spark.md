# Wrangling data with Spark
- Wrangling data with Spark
- Functional programming
- Read in and write out data
- Spark environment and Spark APIs
- RDD API

## Spark
- written in Scala
- uses functional programming techniques
    - useful for distributed computing
    - python is not functional, some issues can occur
    - PySpark is Python the API for Spark
    - functions should not affect the environment
    - functions should not preserve inputs - pure functions
- will not mutate data
- uses lazy evaluation to not run of memory
    - uses DAGs of operations
    - uses the data as late as possible - stages of multistep combos

## PySpark
- SparkContext - provides an entry point to Spark
- parallelize - converts a Python list to a distributed spark dataset
- map - can apply a function over the data
- collect - get all results locally
- SparkConf - provide some config values to the Context
- SparkSession - SQL equivalent to the SparkContext

## Distributed data stores
- fault tolerant
- split data through the cluster in chunks

## Imperative programming
- with Spark DataFrames & Python
- concerned with How
- more focused on the stapes taken to get to the result
- eg. DataFrames in pandas

## Declarative programming
- with SQL
- concerned with What
- more focused on the results

## Wrangle data
- ```df = spark.read.json(path)``` - read the data formatted as json
- ```df.printSchema()``` - see columns, types and is_nullable
- ```df.describe``` - see columns and types
- ```df.show(n=1)``` - show first row nicely formatted
- ```df.take(5)``` - fetch first 5 Rows()
- ```df.select("field").show()``` - select a specific field and show it
- ```df.write.save(out_path, format="csv", header=True)``` - write the data to a csv
- ```df = spark.read.csv(out_path, header=True)``` - read back the data from csv
- ```df.count()``` - count all rows
- ```df.filter( df.field == "abc" )``` - filter by field value
- ```df.where()``` - alias for ```filter()```
- ```div_100 = udf(lambda x: x/100 )``` - user defined function that divides values by 100
- ```df.wutgCikynb( "new_field", div_100(df.field) )``` - generate new column by applying udf on column
- ```df.groupby(df.field).orderBy(df.field)``` - group by and order by example
- ```df_pd = df.toPandas()``` - convert spark DataFrame to pandas
- ```df.dropna(how="any", subset=["field1", "field2"])``` - drop empty values
- ```df.duplicates()``` - drop duplicates
- ```df2 = df.filter(df.field != "")``` - filter empty fields
- Window function example - split user activity before and after downgrade
    ```
    windowval = Window.partitionBy("userId")
          .orderBy(desc("ts"))
          .rangeBetween(Windows.unboundedPreceding, 0)
    df3 = df.withColumn("phase, Fsum("downgraded".over(windowval))")
    ```
- Aggregate functions: ```count()```,```countDistinct()```,```avg()```,```max()```,```min()```

## Spark SQL resources

Here are a few resources that you might find helpful when working with Spark SQL

-   [Spark SQL built-in functions](https://spark.apache.org/docs/latest/api/sql/index.html)
-   [Spark SQL guide](https://spark.apache.org/docs/latest/sql-getting-started.html)
- queries are all optimized by Spark SQL Optimizer - Catalyst
- start with ```df.createOrReplaceTempView("view_name")``` - create a temporary view
- ```spark.sql("SELECT * FROM view_name LIMIT 2").show()``` - select 2 rows example
- ```spark.udf.register("div_100", lambda x: x/100)``` - define an UDF in Spark SQL

# RDDs
- Resilient Distributed Data Set
- SQL or DataFrame -> Optimizer -> Execution plan (DAG) -> RDD
- Spark version
    - < 1.3 RDD
    - = 1.4 DataFrame API
    - 2.0 DataFrame & Datasets API were unified
- More flexibility
- code is harder to read on write
- can't use Optimizer

