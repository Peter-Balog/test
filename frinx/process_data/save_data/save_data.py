import psycopg2
from psycopg2.extras import Json


class SaveDataPostgreSQL:
    """
    Creates table and saves data to PostgreSQL.
    """
    HOSTNAME: str = 'localhost'
    DATABASE: str = 'postgres'
    USER: str = 'postgres'
    PASSWORD: str = 'password'
    PORT: int = 5432

    def __init__(self):
        self.cursor = None
        self.connection = None
        self.connect()
        self.crate_table()

    def connect(self, host: str = HOSTNAME, database: str = DATABASE, user: str = USER, password: str = PASSWORD,
                port: int = PORT) -> None:
        """
        Establishes connection and cursor to PostgreSQL.

        :param host: host name
        :param database: the name of the database
        :param user: user ID
        :param password: password which is has been already set by PostgreSQL
        :param port: database port
        """
        # establishing the connection
        try:
            self.connection = psycopg2.connect(host=host,  database=database, user=user, password=password, port=port)

            # Creating a cursor object using the cursor() method
            self.cursor = self.connection.cursor()
        except Exception as error:
            print(error)

    def crate_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS device_table')

        # define each column for the table in the database
        table = '''CREATE TABLE device_table (
                                                id                SERIAL PRIMARY KEY,
                                                name              varchar(255) NOT NULL,
                                                description       varchar(255),
                                                config            json,
                                                port_channel_id   int,
                                                max_frame_size    int
                                                )'''

        # create table and commit
        self.cursor.execute(table)
        self.connection.commit()

    def add_data_to_table(self, name: str = None, description: str = None, config: dict = None,
                          port_channel_id: int = None, max_frame_size: int = None) -> None:
        """
        Adds data to the table line by line.

        :param name: device interface with name
        :param description: description of the device
        :param config: configuration of the device
        :param port_channel_id: the channel id of the device
        :param max_frame_size: the frame size of the device
        """
        data_to_insert = 'INSERT INTO device_table (name, description, config, port_channel_id,' \
                         ' max_frame_size) VALUES (%s, %s, %s, %s, %s)'
        config = (Json(config),)
        values_to_insert = (name, description, config, port_channel_id, max_frame_size)
        self.cursor.execute(data_to_insert, values_to_insert)
        self.connection.commit()

    def close(self) -> None:
        """
        Closes the cursor and connection to the PostgreSQL.
        """
        self.cursor.close()
        self.connection.close()
