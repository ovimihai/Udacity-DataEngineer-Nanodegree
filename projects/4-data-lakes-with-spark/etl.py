import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, dayofweek, weekofyear
from pyspark.sql.types import TimestampType
from pyspark.sql.functions import monotonically_increasing_id


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['default']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['default']['AWS_SECRET_ACCESS_KEY']
SOURCE=config['default']['SOURCE']
OUTPUT=config['default']['OUTPUT']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "com.amazonaws:aws-java-sdk-pom:1.10.34,org.apache.hadoop:hadoop-aws:2.7.2") \
        .config("key.converter", "org.apache.kafka.connect.storage.StringConverter") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """Process song_data
    
    Fetch song_data form the input folder (local or S3)
    Create dimension tables for songs and artists
    Write the results partitioned songs by year and artist
    Write the artist to parquet
    
    Args:
        spark: SparkSession
        input_data: Input Path (local or S3)
        output_data: Output path (local or S3)
    Returns:
        None    
    """
    
    print("Loading song_data")
    # get filepath to song data file
    song_data = os.path.join(input_data, 'song_data/*/*/*/*.json')
    
    # read song data file
    df = spark.read.json(song_data)
    print("Loaded %d songs " % df.count())
    # print(df.printSchema())

    # extract columns to create songs table
    songs_table = df.select("song_id", "title", "artist_id", "artist_name", "year", "duration").dropDuplicates()
    
    print("Writing songs table to parquet")
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode("overwrite").partitionBy("year", "artist_id").parquet(output_data + 'songs/')

    # extract columns to create artists table
    artists_table = df.selectExpr( [
            "artist_id",
            "artist_name as name",
            "artist_location as location", 
            "artist_latitude as latitude",
            "artist_longitude as longitude"]
        ).dropDuplicates()
    
    print("Writing artists table to parquet")
    # write artists table to parquet files
    artists_table.write.mode("overwrite").parquet(output_data + 'artists/')


def process_log_data(spark, input_data, output_data):
    """Process log_data
    
    Process log_data from the input path(local or S3)
    Create dimension tables for users, time and songplays fact table
    
    Args:
        spark: SparkSession
        input_data: Input Path (local or S3)
        output_data: Output path (local or S3)
    Returns:
        None 
    """
    
    print("Loading log_data")
    # get filepath to log data file
    log_data = os.path.join(input_data,"log_data/*/*/*.json")

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.where(col("page")=="NextSong")
    print("Loaded %d log actions " % df.count())

    # extract columns for users table    
    users_table = df.select("userId", "firstName", "lastName", "gender", "level","ts") \
        .orderBy("ts",ascending=False) \
        .dropDuplicates(subset=["userId"]) \
        .drop('ts')
    
    print("Writing users data")
    # write users table to parquet files
    users_table.write.mode("overwrite").parquet(os.path.join(output_data, "users/"))


    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: datetime.fromtimestamp(int(int(x)/1000)), TimestampType())
    
    # build start_time column and year and month for partitioning
    df = df.withColumn("start_time", get_timestamp(df.ts)) \
        .withColumn("month", month(col("start_time"))) \
        .withColumn("year", year(col("start_time")))
    
    # extract columns to create time table
    time_table = df.select("start_time", "month", "year").dropDuplicates() \
        .withColumn("hour", hour(col("start_time"))) \
        .withColumn("day", dayofmonth(col("start_time"))) \
        .withColumn("week", weekofyear(col("start_time"))) \
        .withColumn("weekday", dayofweek(col("start_time")))
        
    
    print("Writing time data")
    # write time table to parquet files partitioned by year and month
    time_table.write.mode("overwrite") \
        .partitionBy("year", "month") \
        .parquet(os.path.join(output_data, 'time/'))

    # read in song data to use for songplays table
    song_df = spark.read.parquet(os.path.join(output_data, 'songs/')).withColumnRenamed("year", "song_year")

    print("Joining logs with songs data")
    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = df.join(song_df,
        (df.artist == song_df.artist_name) & (df.song == song_df.title) & (df.length == song_df.duration),
        how='inner')
    
    print("Loaded %d songplays " % songplays_table.count())
    
    songplays_table = songplays_table.withColumn("songplay_id", monotonically_increasing_id())
    
    print("Writing songplays data")
    # write songplays table to parquet files partitioned by year and month
    songplays_table.selectExpr( [
         "songplay_id",
         "start_time",
         "userId as user_id",
         "level",
         "song_id",
         "artist_id", 
         "sessionId as session_id",
         "location",
         "userAgent as user_agent",
         "year",
         "month" ]) \
        .write.mode("overwrite") \
        .partitionBy("year", "month") \
        .parquet(output_data + "songplays/")


def main():
    
    spark = create_spark_session()
    input_data = SOURCE
    output_data = OUTPUT
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)

    
if __name__ == "__main__":
    main()
