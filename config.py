import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()


def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("host"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            database=os.getenv("database"),
        )

        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Connection error: {e}")
        return None


def create_database():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("host"),
            user=os.getenv("user"),
            password=os.getenv("password"),
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS userServer")
        print("Database 'userServer' created or already exists.")
    except Error as e:
        print(f"Database creation error: {e}")
    finally:
        cursor.close()
        connection.close()


def create_table(connection):
    try:
        cursor = connection.cursor()
        query1 = """
        CREATE TABLE IF NOT EXISTS user (
            uuid CHAR(32),
            email VARCHAR(120) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created DATETIME NOT NULL,
            updated DATETIME NOT NULL,
            PRIMARY KEY(uuid)
        );
        """
        cursor.execute(query1)

        query2 = """
        CREATE TABLE IF NOT EXISTS studysession (
            id INT AUTO_INCREMENT,
            user_uuid CHAR(32) NOT NULL,
            email VARCHAR(120) NOT NULL,
            subject VARCHAR(255),
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL,
            waste_time TIME,
            real_time TIME,
            PRIMARY KEY (id),
            FOREIGN KEY (user_uuid) REFERENCES user(uuid) ON DELETE CASCADE,
            FOREIGN KEY (email) REFERENCES user(email)
        );
        """
        cursor.execute(query2)

        query3 = """
        CREATE TRIGGER calculate_real_time
        BEFORE INSERT ON studysession
        FOR EACH ROW
        BEGIN
            SET NEW.real_time = TIMEDIFF(
                TIMEDIFF(NEW.end_time, NEW.start_time),
                COALESCE(NEW.waste_time, '00:00:00')
            );
        END;
        """
        cursor.execute(query3, multi=True)

        connection.commit()
        print("Tables and trigger created successfully.")
    except Error as e:
        print(f"Table creation error: {e}")
    finally:
        cursor.close()


if __name__ == "__main__":
    create_database()
    conn = create_connection()
    if conn:
        create_table(conn)
        conn.close()