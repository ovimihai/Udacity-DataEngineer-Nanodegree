# Spark Clusters in AWS

## Steps
0. Create a [Key Pair](https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#KeyPairs:)
0. Create an [EMR cluster](https://us-west-2.console.aws.amazon.com/elasticmapreduce/home?region=us-west-2#)
    - fill name, Release: ```emr-5.20.0```, Applications: Spark
    - instance type ```m5.xlarge```
    - core nodes: 4
    - select SSH key
    - Create cluster

*[AWS machine types](https://aws.amazon.com/ec2/instance-types/)*
- letter
    - M - multipurpose
    - C - optimized for CPU
    - R - optimized for RAM
- number - generation of hardware
    - 5 = 5th generation, comes with SSD
- size: ```nano```, ```small```, ```medium```, ```large```, ```xlarge```


## Spark Scripts
- add needed imports
- define the spark Session
- won't have ```sc``` alias by default
- need __main__ python defined to run as a module
- need to ```spark.stop()``` at the end
- ```spark-submit --master yarn file.py```
- after the submit
    - will output a lot of INFOs
    - make sure warnings or errors won't affect your job
    - output is shown inline - should put in a file

## S3 - Simple Storage Service
- Safe, easy to use, cheap
- ```df = spark.read.load("s3://my_bucket/path/to/file/file.csv")``` read data

[Git repo with details](https://github.com/udacity/nd027-c3-data-lakes-with-spark), 
[Amazon ERM](https://docs.aws.amazon.com/code-samples/latest/catalog/python-emr-emr_basics.py.html)

## HDFS commands
- ```hdfs dfs -mkdir /spark/data``` - create a folder
- ```hdfs dfs -copyFromLocal file.json /spark/data/file.json``` - copy from local to HDFS
- ```df = spark.read.json("hdfs:///spark/data/file.json")``` read data from HDFS



## Extra
- create EMR user with the following rights
    ```
    AmazonElasticMapReduceEditorsRole
    AmazonElasticMapReduceRole
    AmazonElasticMapReduceforEC2Role
    AmazonElasticMapReduceReadOnlyAccess
    AmazonElasticMapReduceFullAccess
    AmazonElasticMapReduceforAutoScalingRole
    AmazonElasticMapReducePlacementGroupPolicy
    ```