from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
import json
import requests

LATITUDE = 37.7749
LONGITUDE = -122.4194

POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'api.open-meteo.com'

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

## DAG

with DAG(
    # DAG ID
    dag_id='waether_etl_pipline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:
## Tasks
    @task()
    def extract():
        """Extract data from the weather API"""
        api_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')
        ## Build the API URL
        ## https://api.open-meteo.com/v1/forecast?latitude=37.7749&longitude=-122.4194&daily=7&timezone=America/Los_Angeles
        endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America/Los_Angeles'

        ## Make the API request
        response = api_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to fetch data from the weather API {response.status_code}')
      

    @task()
    def transform(response: dict):
        """Transform the extracted data"""
        daily_data = response['daily']
        transformed_data = []

        for i in range(len(daily_data['time'])):
            transformed_data.append({
                'date': daily_data['time'][i],
                'latitude': LATITUDE,
                'longitude': LONGITUDE,
                'temperature_max': daily_data['temperature_2m_max'][i],
                'temperature_min': daily_data['temperature_2m_min'][i],
                'precipitation': daily_data['precipitation_sum'][i],
            })

        return transformed_data

    @task()
    def load(transformed_data: list):
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_weather (
                date DATE,
                latitude FLOAT,
                longitude FLOAT,
                temperature_max FLOAT,
                temperature_min FLOAT,
                precipitation FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        # Insert the data into the table
        for record in transformed_data:
            cursor.execute('''
                INSERT INTO daily_weather (date, latitude, longitude, temperature_max, temperature_min, precipitation)
                VALUES (%s, %s, %s, %s, %s, %s);
            ''', (record['date'], record['latitude'], record['longitude'], record['temperature_max'], record['temperature_min'], record['precipitation']))

        conn.commit()
        cursor.close()
        
 ## DAG Workflow ETL Pipeline
    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)