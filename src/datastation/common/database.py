import psycopg


class Database:

    def __init__(self, config):
        self.host = config['host']
        self.dbname = config['dbname']
        self.user = config['user']
        self.password = config['password']
        self.connection = None

    def connect(self):
        self.connection = psycopg.connect(
            f"host={self.host} dbname={self.dbname} user={self.user} password={self.password}")

    def query(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def update(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def close(self):
        if self.connection is not None:
            self.connection.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
