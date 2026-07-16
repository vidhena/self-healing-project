import docker

client = docker.from_env()

def get_all_containers():
    containers = client.containers.list(all=True)

    container_list = []

    for container in containers:
        container_list.append({
            "id": container.short_id,
            "name": container.name,
            "status": container.status,
            "image": container.image.tags[0] if container.image.tags else "No Tag"
        })

    return container_list