from flask import Flask, request, Response
import json, time

app = Flask(__name__)

@app.route("/")
def get_highscores():
    user_id = request.args.get("user_id")
    score = request.args.get("score")
    msg_id = request.args.get("msg_id")
    if not (user_id and score and msg_id):
        return Response("false")
    with open("data.json", "r") as f:
        data = json.load(f)
        data.append({"user_id":user_id, "msg_id":msg_id, "score":score, "time":time.time()})
    with open("data.json", "w") as f:
        json.dump(data, f)
    
    return Response("Done")

