import docker
import pytest
import random
import string
from resources.objects.mysql import mysqlClient
from resources.objects.config.config import configClass
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


@pytest.fixture(scope="function", name='generate_random')
def generate_random_for_table_creation(mariadb_client):
    random_name = ''.join(random.choices(string.ascii_lowercase, k=10))
    yield random_name

    # This fixture is to be used when we want to create a table with a random substring. Clean it if exists
    mariadb_client.delete_table_containing_string(random_name)


@pytest.fixture(scope="session")
def config():
    yield configClass()
