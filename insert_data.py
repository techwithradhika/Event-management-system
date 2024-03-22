import mysql.connector
import csv

def insert_data_from_csv(csv_file):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="events_database"
    )
    cursor = connection.cursor()

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
                INSERT INTO events (event_name, city_name, date, time, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (row['event_name'], row['city_name'], row['date'], row['time'], row['latitude'], row['longitude']))
    
    connection.commit()
    connection.close()
    print("Data inserted from CSV into the database.")

if __name__ == "__main__":
    csv_file = 'events.csv'  # Specify the CSV dataset file path
    insert_data_from_csv(csv_file)
