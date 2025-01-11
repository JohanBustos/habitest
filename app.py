from server import Server, HttpMethod

app = Server()


@app.route("/ping", HttpMethod.GET)
def hello(request, body):
    print(body)
    return {"message": "pong"}


if __name__ == "__main__":
    app.start(port=8081)
