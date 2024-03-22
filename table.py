import mysql.connector

def create_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
    )
    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS events_database")

    cursor.execute("USE events_database")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INT AUTO_INCREMENT PRIMARY KEY,
            event_name VARCHAR(255),
            city_name VARCHAR(255),
            date DATE,
            time TIME,
            latitude DECIMAL(10, 8),
            longitude DECIMAL(11, 8)
        )
    ''')
    
    connection.close()
    print("Database and table created successfully.")

if __name__ == "__main__":
    create_database()
