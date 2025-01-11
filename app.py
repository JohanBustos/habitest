import os

from server import Server, HttpMethod
from database_manager import DatabaseConnection

from src.property.model import Property

cnn = DatabaseConnection(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

cnn.connect()

app = Server()


@app.route("/ping", HttpMethod.GET)
def hello(request, body):
    return {"message": "pong"}


@app.route("/property", HttpMethod.POST)
def get_propieties(request, body):
    properties = Property.find()
    return {"message": properties}


if __name__ == "__main__":
    app.start(port=8081)
