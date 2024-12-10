import uuid
import io
from datetime import datetime, time

from PIL import Image

from config import create_connection
from opencv_detector_yolov11 import detect_phone_yolo


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
            current_date = datetime.now()

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
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user WHERE uuid = %s", (data["uuid"],))
            existing_user = cursor.fetchone()

            if not existing_user:
                return None, "User not found!"

            current_date = datetime.now()

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
    def delete_user(uuid):
        connection = create_connection()
        if connection is None:
            return None, "Failed to connect to the database"

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user WHERE uuid = %s", (uuid,))
            existing_user = cursor.fetchone()

            if not existing_user:
                return None, "User not found!"

            delete_query = "DELETE FROM user WHERE uuid = %s"
            cursor.execute(delete_query, (uuid,))
            connection.commit()

            return True, None
        except Exception as e:
            return None, str(e)
        finally:
            cursor.close()
            connection.close()

class DetectModel:
    @staticmethod
    def detect_phone(data):
        try:
            if not data:
                return None, "No data received"
            imageData = Image.open(io.BytesIO(data))
            num_objects, confidences = detect_phone_yolo(imageData)

            return {"num_objects": num_objects, "confidences": confidences}, None
        except OSError as e:
            return None, f"Invalid image data: {str(e)}"
        except Exception as e:
            return None, f"Error: {str(e)}"

    @staticmethod
    def upload_post(data):
        connection = create_connection()
        if connection is None:
            return None, "Failed to connect to the database"

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user WHERE uuid = %s", (data["uuid"],))
            userData = cursor.fetchall()

            if not userData:
                return None, "Error, it's not user"



            start_time = datetime.strptime(data["start_time"], "%a, %d %b %Y %H:%M:%S %Z")
            end_time = datetime.strptime(data["end_time"], "%a, %d %b %Y %H:%M:%S %Z")

            waste_time_parts = data["waste_time"].split(":")
            waste_time = time(
                hour=int(waste_time_parts[0]),
                minute=int(waste_time_parts[1]),
                second=int(waste_time_parts[2])
            )

            insert_query = """
                INSERT INTO studySession (user_uuid, email, subject, start_time, end_time, waste_time) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
            cursor.execute(
                insert_query,
                (
                    data["uuid"],
                    userData[0][1],
                    data["subject"],
                    start_time,
                    end_time,
                    waste_time,
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
    def get_post():
        connection = create_connection()
        if connection is None:
            return None, "Failed to connect to the database"

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM studysession")
            get_post = cursor.fetchall()

            if not get_post:
                return None, "Post not found!"

            posts = []
            for post in get_post:
                post_data = {
                    "user_uuid": post["user_uuid"],
                    "email": post["email"],
                    "subject": post["subject"],
                    "start_time": post["start_time"],
                    "end_time": post["end_time"],
                    "waste_time": str(post["waste_time"]),
                    "real_time": str(post["real_time"]),
                }
                posts.append(post_data)
            return posts, None

        except Exception as e:
            return None, f"Error: {str(e)}"

    @staticmethod
    def get_post_by_uuid(uuid):
        connection = create_connection()
        if connection is None:
            return None, "Failed to connect to the database"
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user WHERE uuid = %s", (uuid,))
            existing_user = cursor.fetchone()

            if not existing_user:
                return None, "User not found!"

            cursor.execute("SELECT * FROM studysession WHERE user_uuid = %s ORDER BY start_time", (uuid,))
            get_post = cursor.fetchall()

            if not get_post:
                return None, "Post not found!"

            posts = []
            for post in get_post:
                post_data = {
                    "user_uuid": post["user_uuid"],
                    "email": post["email"],
                    "subject": post["subject"],
                    "start_time": post["start_time"],
                    "end_time": post["end_time"],
                    "waste_time": str(post["waste_time"]),
                    "real_time": str(post["real_time"]),
                }
                posts.append(post_data)
            return posts, None

        except Exception as e:
            return None, f"Error: {str(e)}"