import time


def search_container(docker_client, container_name):
    for container in docker_client.containers.list():
        if container.labels['name'] == container_name:
            return container
    else:
        return False
        
def wait_for_container_to_have_status(docker_client, container_name, status, timeout=20):
    initial_ts = int(time.time())
    while int(time.time()) < initial_ts + timeout:
        container = search_container(docker_client, container_name)
        if container and container.status == status:
            break
        time.sleep(0.5)
    else:
        assert False, f'Container status is {container.status} after {timeout} seconds'
