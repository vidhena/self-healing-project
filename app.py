from flask import Flask, render_template, redirect, url_for
import docker

app = Flask(__name__)

client = docker.from_env()


@app.route("/")
def dashboard():
    containers = client.containers.list(all=True)

    container_list = []

    for container in containers:
        container_list.append({
            "id": container.short_id,
            "name": container.name,
            "image": container.image.tags[0] if container.image.tags else "No Tag",
            "status": container.status
        })

    return render_template("dashboard.html", containers=container_list)


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