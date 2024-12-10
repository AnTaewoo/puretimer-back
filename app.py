from flask import Flask
from config import create_database, create_connection, create_table
from view.view import app_route
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(app_route)

if __name__ == "__main__":
    create_database()
    connection = create_connection()
    if connection:
        create_table(connection)
        connection.close()
    app.run(debug=True, host="0.0.0.0", port=8080)
