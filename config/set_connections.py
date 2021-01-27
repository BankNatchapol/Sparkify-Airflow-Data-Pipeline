from airflow import settings
from airflow.models import Connection

import configparser
config = configparser.ConfigParser()

aws_conn = Connection(
        conn_id=config.get('AWS', 'CONN_ID'),
        conn_type=config.get('AWS','CONN_TYPE'),
        login=config.get('AWS','LOGIN'),
        password=config.get('AWS','PASSWORD'),
) 

redshift_conn = Connection(
        conn_id=config.get('REDSHIFT', 'CONN_ID'),
        conn_type=config.get('REDSHIFT','CONN_TYPE'),
        host=config.get('REDSHIFT','CONN_TYPE'),
        schema=config.get('REDSHIFT','DWH_DB'),
        login=config.get('REDSHIFT','DWH_DB_USER'),
        password=config.get('REDSHIFT','DWH_DB_PASSWORD'),
        port=config.get('REDSHIFT','DWH_PORT')
) 

session = settings.Session() 
session.add(aws_conn)
session.add(redshift_conn)
session.commit() 