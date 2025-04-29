def test_dir_exist():
    import os
    from db import MYSQL_DATA_DIR
    assert os.path.exists(MYSQL_DATA_DIR)


def test_docker_service():
    import subprocess
    from db import DOCKER_MYSQL_CONTAINER_NAME
    result = subprocess.run(['docker', 'ps'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode()
    assert DOCKER_MYSQL_CONTAINER_NAME in output


def test_initial_connection():
    import mysql.connector
    from db import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT, MYSQL_HOST
    with mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
    ) as conn:
        assert conn.is_connected()
