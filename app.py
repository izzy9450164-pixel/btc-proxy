import os, json, urllib.request
from flask import Flask, request, jsonify
app = Flask(__name__)
KEY = os.environ.get("KEY","")

@app.route('/ai', methods=['POST'])
def ai():
    prompt = request.json.get("prompt","")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps({"model":"claude-sonnet-4-20250514","max_tokens":300,
            "messages":[{"role":"user","content":prompt}]}).encode(),
        headers={"Content-Type":"application/json",
                 "anthropic-version":"2023-06-01","x-api-key":KEY})
    with urllib.request.urlopen(req,timeout=10) as r:
        data = json.loads(r.read())
    text = "".join(b.get("text","") for b in data.get("content",[]))
    return jsonify({"text":text})
