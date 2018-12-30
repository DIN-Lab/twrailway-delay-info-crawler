import mysql.connector
from ptx import PTX
from dotenv import load_dotenv
from os import environ as ENV


load_dotenv()

ptx = PTX(ENV['APP_ID'], ENV['APP_KEY'])
response_data = ptx.get('/Rail/TRA/LiveTrainDelay', {'$format': 'JSON'}).json()

conn = mysql.connector.connect(user=ENV['DB_USER'], password=ENV['DB_PASSWORD'],
                               host=ENV['DB_HOST'], port=ENV['DB_PORT'],
                               database=ENV['DB_NAME'])
cursor = conn.cursor()

db_creation_sql = '''
    CREATE TABLE IF NOT EXISTS
    delay_infos (
        train_id INT,
        station_id INT,
        delay_time INT,
        updated_at TIMESTAMP,
        PRIMARY KEY (train_id, station_id, updated_at)
    )
'''
cursor.execute(db_creation_sql)

insertion_sql = '''
    INSERT IGNORE INTO delay_infos
    (train_id, station_id, delay_time, updated_at)
    VALUES
    (%s, %s, %s, %s)
'''

for entry in response_data:
    delay_time = int(entry['DelayTime'])

    train_id = int(entry['TrainNo'])
    station_id = int(entry['StationID'])
    updated_at = entry['SrcUpdateTime']
    params = (train_id, station_id, delay_time, updated_at)
    cursor.execute(insertion_sql, params)

conn.commit()

cursor.close()
conn.close()
