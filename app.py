from flask import Flask, render_template, redirect, url_for
import docker
import os

app = Flask(__name__)

client = docker.from_env()


@app.route("/")
def dashboard():

    containers = client.containers.list(all=True)

    container_list = []

    running = 0
    stopped = 0

    for container in containers:

        if container.status == "running":
            running += 1
        else:
            stopped += 1

        container_list.append({
            "id": container.short_id,
            "name": container.name,
            "image": container.image.tags[0] if container.image.tags else "No Tag",
            "status": container.status
        })

    total = len(container_list)

    log_file = "logs/incidents.log"

    logs = []

    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            logs = file.readlines()
            logs.reverse()
    else:
        logs = ["No incidents found."]

    return render_template(
        "dashboard.html",
        containers=container_list,
        total=total,
        running=running,
        stopped=stopped,
        logs=logs
    )


@app.route("/start/<container_name>")
def start_container(container_name):

    try:
        container = client.containers.get(container_name)
        container.start()
    except Exception as e:
        print(e)

    return redirect(url_for("dashboard"))


@app.route("/stop/<container_name>")
def stop_container(container_name):

    try:
        container = client.containers.get(container_name)
        container.stop()
    except Exception as e:
        print(e)

    return redirect(url_for("dashboard"))


@app.route("/restart/<container_name>")
def restart_container(container_name):

    try:
        container = client.containers.get(container_name)
        container.restart()
    except Exception as e:
        print(e)

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)