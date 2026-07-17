import docker
import os
from datetime import datetime

client = docker.from_env()

CONTAINER_NAME = "flask-monitor"

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "incidents.log")


def write_log(message):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    with open(LOG_FILE, "a") as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {message}\n")


try:
    container = client.containers.get(CONTAINER_NAME)

    container.reload()

    if container.status == "running":
        print(f"{CONTAINER_NAME} is running.")
        write_log(f"{CONTAINER_NAME} is running.")

    else:
        print(f"{CONTAINER_NAME} stopped. Restarting...")
        write_log(f"{CONTAINER_NAME} stopped. Restarting...")

        container.restart()

        print(f"{CONTAINER_NAME} restarted successfully.")
        write_log(f"{CONTAINER_NAME} restarted successfully.")

except docker.errors.NotFound:
    msg = f"Container '{CONTAINER_NAME}' not found."
    print(msg)
    write_log(msg)


