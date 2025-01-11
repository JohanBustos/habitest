from typing import Union, Dict, Any
import json
from .model import Property, PropertySerializer


class PropertyService:

    def _valid_filters_state(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        ALLOWED_STATE = ["pre_venta", "en_venta", "vendido"]
        filter_state = filters.get("state")
        if not filter_state:
            filters["state"] = ALLOWED_STATE
        if isinstance(filter_state, str):
            filters["state"] = (
                filter_state if filter_state in ALLOWED_STATE else ALLOWED_STATE
            )
        elif isinstance(filter_state, list):
            filters["state"] = [
                state for state in filter_state if state in ALLOWED_STATE
            ]
        return filters

    def get_properties(
        self,
        filters: Dict[str, Any] = None,
        limit: Union[int, None] = None,
        order_by: str = None,
    ):
        if filters is None:
            filters = {}

        filters = self._valid_filters_state(filters)
        properties = Property.find(filters=filters, limit=limit, order_by=order_by)
        result = [
            PropertySerializer.serialize_data(property) for property in properties
        ]
        return {"properties": result}
