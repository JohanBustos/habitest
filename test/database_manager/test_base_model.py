import pytest
from unittest.mock import MagicMock, patch
from database_manager import BaseModel, DatabaseConnection


# Mocking the DatabaseConnection class
class TestModel(BaseModel):
    table = "test_table"


@pytest.fixture
def mock_db_connection():
    """Fixture para mock conexion DB"""
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    patch(
        "database_manager.DatabaseConnection.connect", return_value=mock_connection
    ).start()
    return mock_cursor


def test_base_model_valid_create_attr():
    dict_test = {"name": "test", "age": 20}
    base = BaseModel(**dict_test)
    assert base.name == "test"
    assert base.age == 20


def test_find_with_filters(mock_db_connection):
    # Simulate the query result
    mock_db_connection.fetchall.return_value = [
        ("user_1", 30),  # Simulate a row of data
        ("user_test", 25),
    ]
    mock_db_connection.description = [
        ("name",),
        ("age",),
    ]  # Simulate the column descriptions

    # Set a filter for the find method
    filters = {"name": ["user_1", "user_test"]}

    # Execute the find method
    results = TestModel.find(filters=filters)

    # Verify that the result matches the expected format
    assert len(results) == 2
    assert results[0].name == "user_1"
    assert results[1].name == "user_test"

    # Verify that the mock database was called correctly
    mock_db_connection.execute.assert_called_once_with(
        "SELECT * FROM test_table WHERE name IN (%s, %s)", ["user_1", "user_test"]
    )


def test_find_with_operator_filter(mock_db_connection):
    # Simulate the query result
    mock_db_connection.fetchall.return_value = [
        ("user_1", 30),  # Simulate a row of data
    ]
    mock_db_connection.description = [
        ("name",),
        ("age",),
    ]  # Simulate the column descriptions

    # Set a filter with an operator
    filters = {"age": (">", 25)}

    # Execute the find method
    results = TestModel.find(filters=filters)

    # Verify that the result matches the expected format
    assert len(results) == 1
    assert results[0].name == "user_1"

    # Verify that the mock database was called correctly
    mock_db_connection.execute.assert_called_once_with(
        "SELECT * FROM test_table WHERE age > %s", [25]
    )


def test_find_with_no_results(mock_db_connection):
    # Simulate that there are no results
    mock_db_connection.fetchall.return_value = []
    mock_db_connection.description = [
        ("name",),
        ("age",),
    ]  # Simulate the column descriptions

    # Set a filter
    filters = {"name": ["non_existent_user"]}

    # Execute the find method
    results = TestModel.find(filters=filters)

    # Verify that there are no results
    assert len(results) == 0
