import docker

client = docker.from_env()

CONTAINER_NAME = "flask-monitor"

def get_container():
    return client.containers.get(CONTAINER_NAME)

def get_container_status():
    try:
        container = get_container()
        return {
            "name": container.name,
            "status": container.status
        }
    except Exception:
        return {
            "name": CONTAINER_NAME,
            "status": "Not Found"
        }

def start_container():
    container = get_container()
    container.start()

def stop_container():
    container = get_container()
    container.stop()

def restart_container():
    container = get_container()
    container.restart()