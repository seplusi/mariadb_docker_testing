import docker
import pytest
from resources.objects.mysql import mysqlClient
from resources.objects.docker import search_container, wait_for_container_to_have_status


@pytest.fixture(scope="session")
def mariadb_client():
    docker_client = docker.DockerClient('unix://var/run/docker.sock')
    for image in docker_client.images.list():
        if 'db_server:latest' in image.tags:
            break
    else:
        assert False, f'DB image not found in {docker_client.images.list()}'
    
    if not search_container(docker_client, 'MariaDB Server'):
        # Create docker container with mariadb
        docker_client.containers.run('db_server', ports={'3306/tcp': 9001}, detach=True)
        # Wait for it to have running status
        wait_for_container_to_have_status(docker_client, 'MariaDB Server', 'running')
    
    # Create object to interact with database
    mysql = mysqlClient("127.0.0.1", 9001, "root", "example", 'mydatabase')
    
    yield mysql

    # Teardown
    mysql.close()
