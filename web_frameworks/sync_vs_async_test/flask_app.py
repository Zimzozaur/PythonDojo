from flask import Flask
from time import sleep

app = Flask(__name__)


@app.route('/')
def read_root():
    sleep(3)
    return {"hello": "from Flask"}


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8002)
