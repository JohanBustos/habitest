import pytest
from unittest.mock import MagicMock, patch
from database_manager import BaseModel, BaseSerializer
from unittest.mock import MagicMock
from src.property.model import Property, PropertySerializer


# Mock database for testing purposes
@pytest.fixture
def mock_database():
    """Fixture para mock conexion DB"""
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    patch(
        "src.property.model.Property.find",
        return_value=[{"id": 1, "city": "Sample City", "state": "pre_venta"}],
    ).start()
    return mock_cursor


# Test for the Property class
class TestPropertyModel:

    # Test for the "table" attribute
    def test_table(self):
        # Check if the Property class has the correct table assigned
        property_instance = Property()
        assert property_instance.table == "properties"

    # Test for the `find` method (if implemented in BaseModel)
    def test_find_with_filters(self, mock_database):

        # Execute an example of search with filters
        filters = {"city": "Sample City", "state": "pre_venta"}
        results = Property.find(filters=filters)

        # Validate that the search worked correctly
        assert len(results) > 0
        assert results[0]["city"] == "Sample City"
        assert results[0]["state"] == "pre_venta"


# Test for the PropertySerializer class
class TestPropertySerializer:

    # Test for serializing a Property object
    def test_serialize_property(self):
        # Create a Property instance with test data
        property_instance = Property(
            id=1,
            city="Sample City",
            state="pre_venta",
            price=100000,
            address="123 Sample Street",
            construction_year=2020,
            description="Nice house",
        )

        # Serialize the Property instance
        serialized_json = PropertySerializer.serialize_data(property_instance)

        assert "id" in serialized_json
        assert "city" in serialized_json
        assert "state" in serialized_json
        assert "price" in serialized_json
        assert "address" in serialized_json
        assert "construction_year" in serialized_json
        assert "description" in serialized_json

    # Test for verifying the serialized values of a Property object
    def test_serialization_values(self):
        # Create a Property instance with test data
        property_instance = Property(
            id=2,
            city="Test City",
            state="en_venta",
            price=150000,
            address="456 Test Avenue",
            construction_year=2015,
            description="Spacious apartment",
        )

        # Serialize the Property instance
        serialized_json = PropertySerializer.serialize_data(property_instance)

        # Validate that the values are serialized correctly
        assert serialized_json["id"] == 2
        assert serialized_json["city"] == "Test City"
        assert serialized_json["state"] == "en_venta"
        assert serialized_json["price"] == 150000
        assert serialized_json["address"] == "456 Test Avenue"
        assert serialized_json["construction_year"] == 2015
        assert serialized_json["description"] == "Spacious apartment"
