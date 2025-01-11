import os

import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    """
    Singleton class to manage the database connection.
    Ensures only one connection instance is created and reused across the application.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the Singleton pattern.
        Ensures only one instance of the class is created.

        Returns:
            DatabaseConnection: The single instance of the DatabaseConnection class.
        """
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, host=None, database=None, user=None, password=None):
        """
        Initialize the DatabaseConnection instance with database parameters.
        Parameters are only set during the first initialization.

        Args:
            host (str): Database host.
            database (str): Database name.
            user (str): Username for the database.
            password (str): Password for the database.
        """
        if not self._initialized:
            self._host = host or os.getenv("DB_HOST")
            self._database = database or os.getenv("DB_NAME")
            self._user = user or os.getenv("DB_USER")
            self._password = password or os.getenv("DB_PASSWORD")
            self.connection = None
            self._initialized = True

    def connect(self):
        """
        Establish a connection to the database using the initialized parameters.

        Returns:
            mysql.connector.connection.MySQLConnection: The database connection.

        Raises:
            mysql.connector.Error: If the connection fails.
        """
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=self._host,
                    database=self._database,
                    user=self._user,
                    password=self._password,
                )
                print("Successful connection to the database.")
            except Error as e:
                print(f"Error connecting to the database: {e}")
                raise
        return self.connection

    def close(self):
        """
        Close the database connection.

        If the connection is active, this method closes it to free up resources.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")
