from database_manager import BaseModel, BaseSerializer


class Property(BaseModel):
    table = "properties"


class PropertySerializer(BaseSerializer):
    model = Property
    fields = [
        "id",
        "city",
        "state",
        "price",
        "address",
        "construction_year",
        "description",
    ]
