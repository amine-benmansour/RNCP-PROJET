from kafka import KafkaConsumer
import json
import threading
import time
import datetime
import mysql.connector

try:
    conn = mysql.connector.connect(
        host="mysql",
        user="your_mysql_user",
        password="your_mysql_password",
        database="your_database_name"
    )
    print("Connected to MySQL!")
except Exception as e:
    print("Error:", str(e))
    exit()

cBinance = KafkaConsumer('Binance', bootstrap_servers=['kafka:9093'], api_version=(2, 6, 0))

cursor = conn.cursor()

def convert_milliseconds_to_datetime(milliseconds):
    timestamp_in_seconds = milliseconds / 1000
    datetime_value = datetime.datetime.utcfromtimestamp(timestamp_in_seconds)
    return datetime_value

def add_data_to_table(table_name, data):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    if not cursor.fetchone():
        cursor.execute(f"CREATE TABLE {table_name} ("
            "ID INT AUTO_INCREMENT PRIMARY KEY, "
            "Timestamp DATETIME, "
            "Open DECIMAL(10, 2), "
            "High DECIMAL(10, 2), "
            "Low DECIMAL(10, 2), "
            "Close DECIMAL(10, 2), "
            "Volume DECIMAL(10, 2)"
            ")")
        print(f"Table {table_name} created.")

    for i in data:
        timestamp, open_price, high, low, close, volume = i
        datetime_value = convert_milliseconds_to_datetime(timestamp)
        cursor.execute(
            f"INSERT INTO {table_name} (Timestamp, Open, High, Low, Close, Volume) VALUES (%s, %s, %s, %s, %s, %s)",
            (datetime_value, open_price, high, low, close, volume))

    conn.commit()

def main_binance():
    for msg2 in cBinance:
        data = json.loads(msg2.value)
        add_data_to_table("CoursXRP", data.get("XRP", []))
        add_data_to_table("CoursBTC", data.get("BTC", []))
        add_data_to_table("CoursETH", data.get("ETH", []))

try:
    main_binance()
except Exception as e:
    print("Error:", str(e))

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
