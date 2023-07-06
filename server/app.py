from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = [message.to_dict() for message in Message.query.all()]
        sorted_messages = sorted(messages, key=lambda x: x["created_at"])

        return make_response(sorted_messages, 200)

    elif request.method == "POST":
        request_json = request.get_json()
        new_message = Message(
            body=request_json["body"], username=request_json["username"]
        )

        db.session.add(new_message)
        db.session.commit()

        return make_response(new_message.to_dict(), 201)


@app.route("/messages/<int:id>", methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == "PATCH":
        request_json = request.get_json()
        for key in request_json:
            setattr(message, key, request_json[key])
        db.session.add(message)
        db.session.commit()
        return make_response(message.to_dict(), 200)

    if request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()

        return make_response("Successfully deleted", 204)


if __name__ == "__main__":
    app.run(port=5555)
