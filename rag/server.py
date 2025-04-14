from .chat import text_chat
from flask import Flask
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "!secret"
socketio = SocketIO(app)


@socketio.on("json")
def handle_message(data):
    user_id = data["user_id"]
    messsage = data["query"]
    response = text_chat(message=messsage, user_id=user_id)

    data = {"response": response}

    emit("response", data, json=True)


if __name__ == "__main__":
    socketio.run(app)
