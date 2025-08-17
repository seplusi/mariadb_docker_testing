import random
import string


def test_show_table_users(mariadb_client):
    query = "show tables;"
    assert any([table[0] == 'users' for table in mariadb_client.get_data_from_query(query)])
    

def test_table_description(mariadb_client):
    query = 'desc users;'
    output = mariadb_client.get_data_from_query(query)
    assert len(output) == 3
    assert output[0][:2] == ('id', 'int(11)',)
    assert output[1][:2] == ('username', 'varchar(255)',)
    assert output[2][:2] == ('email', 'varchar(255)')


def test_insert_data_into_users_table(mariadb_client):
    # Insert data
    user = f'seplusi_{"".join(random.choices(string.ascii_lowercase, k=7))}'
    query = f'INSERT INTO users (username, email) VALUES("{user}", "seplusi_arcanjo@hotmail.com")'
    mariadb_client.insert_data(query)

    # Query table to assert on newly added data
    query = 'select * from users'
    output = mariadb_client.get_data_from_query(query)
    for entry in output:
        if entry[1] == user:
            break
    else:
        assert False, f'User seplusi not found in output{output}'

    assert entry[1] == user
    assert entry[2] == 'seplusi_arcanjo@hotmail.com'


def test_create_table(mariadb_client, generate_random):
    table = f'create_test_table_{generate_random}'
    # SQL statement to create the table
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        age INT,
        major VARCHAR(100)
    );
    """

    # Execute the CREATE TABLE statement
    output = mariadb_client.create_table(create_table_sql)
    assert output == [], f'Expected output: []. Got {output} instead.'
    
    # Validate table items are correct
    query = f'desc {table};'
    output = mariadb_client.get_data_from_query(query)
    assert len(output) == 5
    assert output[0][:2] == ('id', 'int(11)',)
    assert output[1][:2] == ('first_name', 'varchar(50)',)
    assert output[2][:2] == ('last_name', 'varchar(50)')
    assert output[3][:2] == ('age', 'int(11)')
    assert output[4][:2] == ('major', 'varchar(100)')
