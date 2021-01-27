from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator, 
                                CreateRedshiftTablesOperator)
from helpers import SqlQueries, CreateTables

AWS_KEY = os.environ.get('AWS_KEY')
AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'Adrien',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 12),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('sparkify_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

songplays_table_create = CreateRedshiftTablesOperator(
    task_id = 'create_songplays_table',
    dag = dag,
    table = 'songplays',
    redshift_conn_id = 'redshift',
    create_table_sql = CreateTables.songplays_table_create
)

artists_table_create = CreateRedshiftTablesOperator(
    task_id = 'create_artist_table',
    dag = dag,
    table = 'artists',
    redshift_conn_id = 'redshift',
    create_table_sql = CreateTables.artists_table_create
)

songs_table_create = CreateRedshiftTablesOperator(
    task_id = 'create_songs_table',
    dag = dag,
    table = 'songs',
    redshift_conn_id = 'redshift',
    create_table_sql = CreateTables.songs_table_create
)

users_table_create = CreateRedshiftTablesOperator(
    task_id = 'create_users_table',
    dag = dag,
    table = 'users',
    redshift_conn_id = 'redshift',
    create_table_sql = CreateTables.users_table_create
)

time_table_create = CreateRedshiftTablesOperator(
    task_id = 'create_times_table',
    dag = dag,
    table = 'times',
    redshift_conn_id = 'redshift',
    create_table_sql = CreateTables.time_table_create
)

staging_events_table_create = CreateRedshiftTablesOperator(
    task_id = 'create_staging_events_table',
    dag = dag,
    table = 'staging_events',
    redshift_conn_id = 'redshift',
    create_table_sql = CreateTables.staging_events_table_create
)

staging_songs_table_create = CreateRedshiftTablesOperator(
    task_id = 'create_staging_songs_table',
    dag = dag,
    table = 'staging_songs',
    redshift_conn_id = 'redshift',
    create_table_sql = CreateTables.staging_songs_table_create
)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id = 'Stage_events',
    dag = dag,
    table = 'staging_events',
    redshift_conn_id = 'redshift',
    aws_credentials_id = 'aws_credentials_id',
    s3_key = s3_logdata_key,
    s3_bucket = s3_bucket,
    JSON_formatting = s3_full_jsonpath,
    append_data = False
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)
