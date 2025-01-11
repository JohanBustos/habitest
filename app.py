import os

from dotenv import load_dotenv

from server import Server, HttpMethod
from database_manager import DatabaseConnection


load_dotenv()

# Check required environment variables
required_env_vars = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD"]
for var in required_env_vars:
    assert os.getenv(var), f"Missing environment variable: {var}"

cnn = DatabaseConnection(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

try:
    cnn.connect()
except Exception as e:
    exit(1)

app = Server()

import src.property.controller


@app.route("/ping", HttpMethod.GET)
def hello(request, body):
    return {"message": "pong"}


if __name__ == "__main__":
    app.start(port=8081)
