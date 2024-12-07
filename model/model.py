import uuid
import datetime
from config import create_connection


class UserModel:
    @staticmethod
    def create_user(data):
        connection = create_connection()
        if connection is None:
            return None, "Failed to connect to the database"

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user WHERE email = %s", (data["email"],))
            existing_user = cursor.fetchall()

            if existing_user:
                return None, "User already exists!"

            user_uuid = uuid.uuid4().hex
            current_date = datetime.datetime.now()

            insert_query = """
            INSERT INTO user (uuid, email, password, created, updated) 
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (
                    user_uuid,
                    data["email"],
                    data["password"],
                    current_date,
                    current_date,
                ),
            )
            connection.commit()

            return user_uuid, None
        except Exception as e:
            return None, str(e)
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def login_user(data):
        connection = create_connection()
        if connection is None:
            return None, "Failed to connect to the database"

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM user WHERE email = %s AND password = %s ",
                (data["email"], data["password"],),
            )
            existing_user = cursor.fetchall()

            if not existing_user:
                return None, "User information incorrect"

            user = existing_user[0]

            return user, None
        except Exception as e:
            return None, str(e)
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_user_by_uuid(user_uuid):
        connection = create_connection()
        if connection is None:
            return None, "Failed to connect to the database"

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user WHERE uuid = %s", (user_uuid,))
            user = cursor.fetchone()
            return user, None if user else "User not found"
        except Exception as e:
            return None, str(e)
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_user(data):
        connection = create_connection()
        if connection is None:
            return None, "Failed to connect to the database"

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user WHERE uuid = %s", (data["uuid"],))
            existing_user = cursor.fetchone()

            if not existing_user:
                return None, "User not found!"

            current_date = datetime.datetime.now()

            update_query = """
            UPDATE user 
            SET password = %s, updated = %s 
            WHERE uuid = %s
            """
            cursor.execute(
                update_query,
                (
                    data["password"],
                    current_date,
                    data["uuid"],
                ),
            )
            connection.commit()

            return True, None
        except Exception as e:
            return None, str(e)
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete_user(user_uuid):
        connection = create_connection()
        if connection is None:
            return None, "Failed to connect to the database"

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user WHERE uuid = %s", (user_uuid,))
            existing_user = cursor.fetchone()

            if not existing_user:
                return None, "User not found!"

            delete_query = "DELETE FROM user WHERE uuid = %s"
            cursor.execute(delete_query, (user_uuid,))
            connection.commit()

            return True, None
        except Exception as e:
            return None, str(e)
        finally:
            cursor.close()
            connection.close()
