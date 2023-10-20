from flask import Flask

app = Flask("HelloWorldApp")


@app.get("/")
async def hello_world():
    return "Hello, world"


app.run()
