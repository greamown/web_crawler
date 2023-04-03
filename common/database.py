# Module Imports
import mariadb, logging, csv
from .utils import read_json

INIT_DATA       =   {
                        "gpu":     "SID MEDIUMINT PRIMARY KEY AUTO_INCREMENT, \
                                    DATETIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
                                    ITEM LONGTEXT NOT NULL, \
                                    PRICE INT NOT NULL"
                    }
# Connect db
def connect():
    # Get connect info in JSON
    db_json = read_json("./common/db.json")
    user = db_json["USER"]
    password = db_json["PASSWORD"]
    host = db_json["HOST"]
    port = db_json["PORT"]
    database = db_json["DBNAME"]
    connector = None
    try:
        # Construct connection string
        connector = mariadb.connect(
            database = database,
            user = user,
            password = password,
            host = host,
            port = port
        )
    except mariadb.Error as e:
        logging.error(f"Error connecting to MariaDB Platform: {e}") 

    return connector

# Execute db
def execute_db(command, update):
    connector = connect()
    db_data, cols = None, None
    try:
        cur = connector.cursor()
        cur.execute(command)
        if not (update):
            db_data = cur.fetchall()
            cols  = cur.description
        cur.close()
        if (update):
            connector.commit()
        return db_data, cols

    except Exception as error:
        logging.error(error)

    finally:
        if connector is not None:
            connector.close()

# Create table
def create_table(table_name, content):
    commands =  """
                CREATE TABLE IF NOT EXISTS {} (
                {}
                )
                """.format(table_name, content)

    return commands

# Initial DB
def init_db():
    connector = connect()
    try:
        cur = connector.cursor()
        for key in INIT_DATA.keys():
            print(key)
            cur.execute(create_table(key, INIT_DATA[key]))
        cur.close()
        connector.commit()
    except Exception as error:
        logging.error(error)

    finally:
        if connector is not None:
            connector.close()

# Add new data in table
def insert_table(table_name, keys, values):
    """ Insert data in tables """
    commands =  """
                INSERT INTO {} ({})
                VALUES ({});
                """.format(table_name, keys, values)
    info_db = execute_db(commands, True)
    return info_db

# Delete data from table
def delete_data_table(table_name, content):
    """ Delete data from tables """
    commands =  """
                DELETE FROM {} WHERE {};
                """.format(table_name, content)
    info_db = execute_db(commands, True)
    return info_db

# Update data from table
def update_data_table(table_name, values, select):
    """ Update data in table """
    commands =  """
                UPDATE {} SET {} WHERE {};
                """.format(table_name, values, select)
    info_db = execute_db(commands, True)
    return info_db

def db_to_csv(path, table_name):
    commands =  '''
                    SELECT * FROM {}
                '''.format(table_name)
    
    info_db = execute_db(commands, False)
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)

        header = [i[0] for i in info_db[-1]]
        writer.writerow(header)
        for row in info_db[0]:
            writer.writerow(row)

def check_data_status(table_name, content):
    commands =  '''
                    SELECT IF(EXISTS ( \
                    SELECT * FROM {} WHERE {}) \
                    ,'true','false') AS result
                '''.format(table_name, content)
    
    info_db = execute_db(commands, False)
    if info_db:
        return info_db[0][0][0]
    return False