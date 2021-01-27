from airflow import settings
from airflow.models import Connection

import configparser
config = configparser.ConfigParser()

conn = Connection(
        conn_id=config.get('AWS', 'CONN_ID'),
        conn_type=config.get('AWS','CONN_TYPE'),
        login=config.get('AWS','LOGIN'),
        password=config.get('AWS','PASSWORD'),
) 
session = settings.Session() 
session.add(conn)
session.commit() 