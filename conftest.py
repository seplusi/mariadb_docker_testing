import docker
import pytest
import mysql.connector


@pytest.fixture(scope="session")
def mariadb_client():
    docker_client = docker.DockerClient('unix://var/run/docker.sock')
    for image in docker_client.images.list():
        if 'db_server:latest' in image.tags:
            break
    else:
        assert False, f'DB image not found in {docker_client.images.list()}'
    
    
    for container in docker_client.containers.list():
        if container.labels['name'] == 'MariaDB Server':
            break
    else:
        assert False, f'Container with MariaDB Server not found'
    
    mysql_client = mysql.connector.connect(host="127.0.0.1", port=9001, user="root", password="example", database='mydatabase')
    yield mysql_client