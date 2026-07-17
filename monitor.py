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

    container_list = []

    running = 0
    stopped = 0

    for container in containers:

        status = container.status

        if status == "running":
            running += 1
        else:
            stopped += 1

        uptime = "-"

        try:
            if status == "running":
                uptime = container.attrs["State"]["StartedAt"]
        except:
            pass

        container_list.append({
            "id": container.short_id,
            "name": container.name,
            "image": container.image.tags[0] if container.image.tags else "No Tag",
            "status": status,
            "uptime": uptime
        })

    total = len(container_list)

    total_images = len(images)

    total_volumes = len(volumes)

    last_updated = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    logs = []

    log_file = "logs/incidents.log"

    if os.path.exists(log_file):

        with open(log_file, "r") as file:

            logs = file.readlines()

            logs.reverse()

    else:

        logs.append("No incidents found.")

    return render_template(
        "dashboard.html",
        containers=container_list,
        total=total,
        running=running,
        stopped=stopped,
        total_images=total_images,
        total_volumes=total_volumes,
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
