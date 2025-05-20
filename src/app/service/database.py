import psycopg2


class SQLError(Exception):
    pass


class Session:
    def __init__(self, config: dict):
        self.configuration = config

    def __enter__(self):
        self.connection = psycopg2.connect(**self.configuration)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        if exc_type is psycopg2._psycopg.Error:
            raise SQLError(exc_value)
        elif exc_type:
            raise exc_type(exc_value)
