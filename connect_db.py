import os
import psycopg2


def get_connection():
    url = os.environ.get('DB_URL')
    connection = psycopg2.connect(url)
    return connection
