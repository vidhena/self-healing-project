from flask import Flask, render_template, redirect, url_for
import docker
import os
from datetime import datetime

app = Flask(__name__)

client = docker.from_env()


@app.route("/")
def dashboard():

    containers = client.containers.list(all=True)
    images = client.images.list()
    volumes = client.volumes.list()
    docker_info = client.version()

    container_list = []

    running = 0
    stopped = 0

    for container in containers:

        status = container.status

        if status == "running":
            running += 1
        else:
            stopped += 1

        cpu = "N/A"
        memory = "N/A"
        uptime = "-"
        health = "Healthy"

        try:
            if status == "running":
                uptime = container.attrs["State"]["StartedAt"]

                stats = container.stats(stream=False)
                mem = stats["memory_stats"]["usage"] / (1024 * 1024)
                memory = f"{mem:.2f} MB"

        except Exception:
            pass

        container_list.append({
            "id": container.short_id,
            "name": container.name,
            "image": container.image.tags[0] if container.image.tags else "No Tag",
            "status": status,
            "cpu": cpu,
            "memory": memory,
            "health": health,
            "uptime": uptime
        })

    total = len(container_list)

    log_file = "logs/incidents.log"

    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            logs = file.readlines()
            logs.reverse()
    else:
        logs = ["No incidents found."]

    total_images = len(images)
    total_volumes = len(volumes)
    docker_version = docker_info["Version"]
    docker_api = docker_info["ApiVersion"]
    last_updated = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    return render_template(
        "dashboard.html",
        containers=container_list,
        total=total,
        running=running,
        stopped=stopped,
        total_images=total_images,
        total_volumes=total_volumes,
        docker_version=docker_version,
        docker_api=docker_api,
        last_updated=last_updated,
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
    