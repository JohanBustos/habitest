from .main import DatabaseConnection


class BaseModel:
    """
    A base class for representing and interacting with database records.
    Provides methods for saving objects to the database and retrieving records
    based on specific conditions.
    """

    table = None

    def __init__(self, **kwargs):
        """
        Initialize a new instance of the model with the provided attributes.

        Args:
            **kwargs: Keyword arguments representing the fields and their values for the model.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = ", ".join(f"{key}={value!r}" for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attrs})"

    @classmethod
    def exec_query(cls, query: str, values: list, map_to_objects=True):
        """
        Executes a SQL query with the given parameters and returns the results.

        Args:
            query (str): The SQL query to be executed.
            values (list): The list of values to be used in the query.
            map_to_objects (bool, optional): Flag to determine if the results should be
                                              mapped to class instances (default is True).

        Returns:
            tuple: A tuple where:
                - The first element is a list of results (rows).
                - The second element is a list of column names (descriptions).
                If `map_to_objects` is True, returns the instances of the class instead of raw data.
        """
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]  # Column names

        # If map_to_objects is True, map the results to class instances
        if map_to_objects:
            objects = []
            for result in results:
                obj = cls(**dict(zip(columns, result)))
                objects.append(obj)
            return objects

        # Otherwise, return raw results (rows) and columns
        return results, columns

    @classmethod
    def find(cls, filters=None, order_by=None, limit=None):
        """
        Find records in the database matching specified filters.

        Args:
            filters (dict, optional): A dictionary where keys are column names and values are:
                                    - A single value for equality filtering (e.g., {"price": 100}).
                                    - A list with an operator and a value (e.g., {"price": [">", 100]}).
                                    - A list of values for IN filtering (e.g., {"name": ["a", "b", "z"]}).
            order_by (str, optional): A column name to sort results by.
            limit (int, optional): Maximum number of results to retrieve.

        Returns:
            list: A list of instances of the current class.
        """
        # Base query
        query = f"SELECT * FROM {cls.table}"
        values = []

        # Allowed operators for filtering
        allowed_operators = {"=", ">", "<", ">=", "<=", "!="}

        # Add WHERE clause if filters are provided
        if filters:
            where_conditions = []
            for key, condition in filters.items():
                if isinstance(condition, list):
                    # Check if it's a filter with an operator
                    if len(condition) == 2 and condition[0] in allowed_operators:
                        operator, value = condition
                        where_conditions.append(f"{key} {operator} %s")
                        values.append(value)
                    else:
                        # Handle IN clause
                        placeholders = ", ".join(["%s"] * len(condition))
                        where_conditions.append(f"{key} IN ({placeholders})")
                        values.extend(condition)
                else:
                    # Default to equality
                    where_conditions.append(f"{key} = %s")
                    values.append(condition)

            # Combine all conditions with AND
            query += f" WHERE {' AND '.join(where_conditions)}"

        # Add ORDER BY clause if specified
        if order_by:
            query += f" ORDER BY {order_by}"

        # Add LIMIT clause if specified
        if limit:
            query += f" LIMIT {limit}"

        results = cls.exec_query(query, values)

        return results
