from flask import Flask
from config import create_database, create_connection, create_table
from view.view import app_route
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(app_route)

if __name__ == "__main__":
    create_database()  # 데이터베이스 생성 (없으면 생성)
    connection = create_connection()
    if connection:
        create_table(connection)  # 테이블 생성 (없으면 생성)
        connection.close()
    app.run(debug=True)
