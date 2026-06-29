from flask import Flask, send_file, request, jsonify
import subprocess, os, time

app = Flask(__name__)
DISPLAY = ":1"
ACTIVITY_FILE = "/tmp/last_activity"


def touch():
    with open(ACTIVITY_FILE, "w") as f:
        f.write(str(time.time()))


@app.route("/api/health")
def health():
    touch()
    return jsonify({"status": "ok", "service": "desktop", "id": os.environ.get("DESKTOP_ID", "?")})


@app.route("/api/screenshot")
def screenshot():
    touch()
    subprocess.run(
        ["scrot", "/tmp/screen.png", "--overwrite"],
        env={**os.environ, "DISPLAY": DISPLAY},
        check=True,
    )
    return send_file("/tmp/screen.png", mimetype="image/png")


@app.route("/api/open", methods=["POST"])
def open_url():
    touch()
    url = request.json.get("url", "")
    if not url:
        return jsonify({"error": "no url"}), 400
    subprocess.Popen(
        [
            "google-chrome",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-software-rasterizer",
            "--memory-pressure-off",
            "--disable-crash-reporter",
            "--no-first-run",
            "--disable-notifications",
            url,
        ],
        env={**os.environ, "DISPLAY": DISPLAY},
    )
    return jsonify({"ok": True, "url": url})


@app.route("/api/type", methods=["POST"])
def type_text():
    touch()
    text = request.json.get("text", "")
    subprocess.run(
        ["xdotool", "type", "--delay", "30", "--", text],
        env={**os.environ, "DISPLAY": DISPLAY},
    )
    return jsonify({"ok": True})


@app.route("/api/click", methods=["POST"])
def click():
    touch()
    x = int(request.json.get("x", 0))
    y = int(request.json.get("y", 0))
    subprocess.run(
        ["xdotool", "mousemove", "--sync", str(x), str(y), "click", "1"],
        env={**os.environ, "DISPLAY": DISPLAY},
    )
    return jsonify({"ok": True, "x": x, "y": y})


@app.route("/api/key", methods=["POST"])
def key_press():
    touch()
    key = request.json.get("key", "")
    subprocess.run(
        ["xdotool", "key", key],
        env={**os.environ, "DISPLAY": DISPLAY},
    )
    return jsonify({"ok": True, "key": key})


@app.route("/api/scroll", methods=["POST"])
def scroll():
    touch()
    direction = request.json.get("direction", "down")
    amount = int(request.json.get("amount", 3))
    button = "5" if direction == "down" else "4"
    for _ in range(amount):
        subprocess.run(
            ["xdotool", "click", button],
            env={**os.environ, "DISPLAY": DISPLAY},
        )
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
