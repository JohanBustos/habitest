import pytest
from unittest.mock import MagicMock
from src.property.service import PropertyService
from src.property.model import Property, PropertySerializer


# Test for the PropertyService class
class TestPropertyService:

    @pytest.fixture
    def property_service(self):
        """Fixture to initialize the PropertyService"""
        return PropertyService()

    # Test for valid state filtering
    def test_valid_filters_state_with_str(self, property_service):
        """Test the _valid_filters_state method when state is a string."""
        filters = {"state": "pre_venta"}
        valid_filters = property_service._valid_filters_state(filters)
        assert valid_filters["state"] == "pre_venta"

    def test_valid_filters_state_with_invalid_str(self, property_service):
        """Test the _valid_filters_state method when state is an invalid string."""
        filters = {"state": "invalid_state"}
        valid_filters = property_service._valid_filters_state(filters)
        assert valid_filters["state"] == ["pre_venta", "en_venta", "vendido"]

    def test_valid_filters_state_with_list(self, property_service):
        """Test the _valid_filters_state method when state is a list."""
        filters = {"state": ["pre_venta", "en_venta"]}
        valid_filters = property_service._valid_filters_state(filters)
        assert valid_filters["state"] == ["pre_venta", "en_venta"]

    def test_valid_filters_state_with_invalid_list(self, property_service):
        """Test the _valid_filters_state method when state is a list with invalid values."""
        filters = {"state": ["invalid_state", "en_venta"]}
        valid_filters = property_service._valid_filters_state(filters)
        assert valid_filters["state"] == ["en_venta"]

    def test_valid_filters_state_no_state(self, property_service):
        """Test the _valid_filters_state method when no state is provided in filters."""
        filters = {}
        valid_filters = property_service._valid_filters_state(filters)
        assert valid_filters["state"] == ["pre_venta", "en_venta", "vendido"]

    # Test for the get_properties method
    def test_get_properties_no_filters(self, property_service):
        """Test the get_properties method with no filters."""
        # Mock the Property.find method to simulate database response
        mock_properties = [
            MagicMock(id=1, city="City A", state="pre_venta", price=100000)
        ]
        Property.find = MagicMock(return_value=mock_properties)

        # Call the service method
        result = property_service.get_properties()

        # Check if the result is correct
        assert "properties" in result
        assert len(result["properties"]) == 1
        assert result["properties"][0]["id"] == 1

    def test_get_properties_with_filters(self, property_service):
        """Test the get_properties method with filters applied."""
        # Mock the Property.find method to simulate database response
        mock_properties = [
            MagicMock(id=1, city="City A", state="pre_venta", price=100000)
        ]
        Property.find = MagicMock(return_value=mock_properties)

        # Apply filters and call the service method
        filters = {"state": "pre_venta"}
        result = property_service.get_properties(filters=filters)

        # Check if the result is correct
        assert "properties" in result
        assert len(result["properties"]) == 1
        assert result["properties"][0]["id"] == 1

    def test_get_properties_with_invalid_filters(self, property_service):
        """Test the get_properties method when invalid filters are applied."""
        # Mock the Property.find method to simulate database response
        mock_properties = [
            MagicMock(id=1, city="City A", state="pre_venta", price=100000)
        ]
        Property.find = MagicMock(return_value=mock_properties)

        # Apply invalid filters
        filters = {"state": "invalid_state"}
        result = property_service.get_properties(filters=filters)

        # The invalid filter should be replaced by the allowed states
        assert "properties" in result
        assert len(result["properties"]) == 1
        assert result["properties"][0]["state"] == "pre_venta"

    def test_get_properties_with_limit(self, property_service):
        """Test the get_properties method with a limit."""
        # Mock the Property.find method to simulate database response
        mock_properties = [
            MagicMock(id=1, city="City A", state="pre_venta", price=100000)
        ]
        Property.find = MagicMock(return_value=mock_properties)

        # Apply filters and limit, then call the service method
        filters = {"state": "pre_venta"}
        result = property_service.get_properties(filters=filters, limit=1)

        # Check if the result respects the limit
        assert len(result["properties"]) == 1

    def test_get_properties_with_order_by(self, property_service):
        """Test the get_properties method with an order_by clause."""
        # Mock the Property.find method to simulate database response
        mock_properties = [
            MagicMock(id=1, city="City A", state="pre_venta", price=100000)
        ]
        Property.find = MagicMock(return_value=mock_properties)

        # Apply filters, limit, and order_by, then call the service method
        filters = {"state": "pre_venta"}
        result = property_service.get_properties(filters=filters, order_by="price")

        # Check if the result contains the ordered properties
        assert len(result["properties"]) == 1
        assert "properties" in result
