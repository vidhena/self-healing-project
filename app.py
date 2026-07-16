from flask import Flask, render_template, redirect

from services.docker_service import (
    get_container_status,
    start_container,
    stop_container,
    restart_container
)

app = Flask(__name__)

@app.route("/")
def dashboard():
    container = get_container_status()
    return render_template("dashboard.html", container=container)

@app.route("/start")
def start():
    start_container()
    return redirect("/")

@app.route("/stop")
def stop():
    stop_container()
    return redirect("/")

@app.route("/restart")
def restart():
    restart_container()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)