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

    @classmethod
    def find(cls, filters=None, order_by=None, limit=None):
        """
        Find records in the database matching specified filters.

        Args:
            filters (dict, optional): A dictionary where keys are column names and values are:
                                      - A single value for equality filtering (e.g., {"price": 100}).
                                      - A tuple with an operator and a value (e.g., {"price": (">", 100)}).
                                      - A list of values for IN filtering (e.g., {"name": ["a", "b", "z"]}).
            order_by (str, optional): A column name to sort results by.
            limit (int, optional): Maximum number of results to retrieve.

        Returns:
            list: A list of instances of the current class.
        """
        query = f"SELECT * FROM {cls.table}"
        values = []

        # Add WHERE clause if filters are provided
        if filters:
            where_conditions = []
            for key, condition in filters.items():
                if isinstance(condition, tuple) and len(condition) == 2:
                    # Handle operators like >, <, >=, <=
                    operator, value = condition
                    where_conditions.append(f"{key} {operator} %s")
                    values.append(value)
                elif isinstance(condition, list):
                    # Handle IN clause
                    placeholders = ", ".join(["%s"] * len(condition))
                    where_conditions.append(f"{key} IN ({placeholders})")
                    values.extend(condition)
                else:
                    # Default to equality
                    where_conditions.append(f"{key} = %s")
                    values.append(condition)

            query += f" WHERE {' AND '.join(where_conditions)}"

        # Add ORDER BY clause if specified
        if order_by:
            query += f" ORDER BY {order_by}"

        # Add LIMIT clause if specified
        if limit:
            query += f" LIMIT {limit}"

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()

        objects = []
        for result in results:
            obj = cls(**dict(zip([desc[0] for desc in cursor.description], result)))
            objects.append(obj)
        return objects
