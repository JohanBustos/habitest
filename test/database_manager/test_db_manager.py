from database_manager import DatabaseConnection


def test_db_valid_uniqued_instance():
    db = DatabaseConnection(
        host="localhost", database="test_db", user="root", password="root"
    )
    db_test = DatabaseConnection(
        host="localhost", database="test_db", user="root", password="root2"
    )
    assert db is db_test
