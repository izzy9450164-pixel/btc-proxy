import os, json, urllib.request, urllib.error
from flask import Flask, request, jsonify

app = Flask(__name__)
KEY = os.environ.get("KEY","")

@app.route('/ai', methods=['POST'])
def ai():
    try:
        prompt = request.json.get("prompt","")
        payload = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 300,
            "messages": [{"role":"user","content":prompt}]
        }).encode()
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
                "x-api-key": KEY
            }
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        text = "".join(b.get("text","") for b in data.get("content",[]))
        return jsonify({"text": text})
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        return jsonify({"error": f"HTTP {e.code}: {error_body}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test')
def test():
    return jsonify({"key_set": bool(KEY), "key_prefix": KEY[:15] if KEY else "EMPTY"})
