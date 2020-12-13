from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'udacity',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
}

dag = DAG('streaming_etl',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *',
          catchup=False,
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    table="staging_events",
    s3_bucket="udacity-dend",
    s3_path="log_data",
    input_format="JSON 's3://udacity-dend/log_json_path.json'",
    extra_params="TIMEFORMAT 'epochmillisecs'",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    region="us-west-2",
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    table="staging_songs",
    s3_bucket="udacity-dend",
    s3_path="song_data",
    input_format="JSON 'auto'",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    region="us-west-2",
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    table='songplays',
    redshift_conn_id="redshift",
    load_sql=SqlQueries.songplay_table_insert,
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    table='users',
    redshift_conn_id="redshift",
    truncate_table=True,
    load_sql=SqlQueries.user_table_insert
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    table='songs',
    redshift_conn_id="redshift",
    truncate_table=True,
    load_sql=SqlQueries.song_table_insert
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    table='artists',
    redshift_conn_id="redshift",
    truncate_table=True,
    load_sql=SqlQueries.artist_table_insert
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    table='time',
    redshift_conn_id="redshift",
    truncate_table=True,
    load_sql=SqlQueries.time_table_insert
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    checks=[
        # check has any data
        { 'sql_check': 'SELECT COUNT(*) FROM public.songplays', 'expected_result': 0, 'operation': 'gt' }, 
        { 'sql_check': 'SELECT COUNT(*) FROM public.artists', 'expected_result': 0, 'operation': 'gt' }, 
        { 'sql_check': 'SELECT COUNT(*) FROM public.songs', 'expected_result': 0, 'operation': 'gt' }, 
        { 'sql_check': 'SELECT COUNT(*) FROM public.users', 'expected_result': 0, 'operation': 'gt' }, 
        { 'sql_check': 'SELECT COUNT(*) FROM public."time"', 'expected_result': 0, 'operation': 'gt' }, 
        # chech has nulls
        { 'sql_check': 'SELECT COUNT(*) FROM public.songplays WHERE userid IS NULL', 'expected_result': 0 }, 
        { 'sql_check': 'SELECT COUNT(*) FROM public.artists WHERE name IS NULL', 'expected_result': 0 },
        { 'sql_check': 'SELECT COUNT(*) FROM public.songs WHERE title IS NULL', 'expected_result': 0 },
        { 'sql_check': 'SELECT COUNT(*) FROM public.users WHERE first_name IS NULL', 'expected_result': 0 },
        { 'sql_check': 'SELECT COUNT(*) FROM public."time" WHERE weekday IS NULL', 'expected_result': 0 },
        # check levels
        { 'sql_check': 'SELECT COUNT(DISTINCT "level") FROM public.songplays', 'expected_result': 2 },
    ],
    redshift_conn_id="redshift",
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> stage_events_to_redshift
start_operator >> stage_songs_to_redshift

stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table

load_songplays_table >> load_time_dimension_table
load_songplays_table >> load_artist_dimension_table
load_songplays_table >> load_song_dimension_table
load_songplays_table >> load_user_dimension_table

load_time_dimension_table >> run_quality_checks
load_artist_dimension_table >> run_quality_checks
load_song_dimension_table >> run_quality_checks
load_user_dimension_table >> run_quality_checks

run_quality_checks >> end_operator






