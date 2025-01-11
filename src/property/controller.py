from server import HttpMethod
from app import app
from .service import PropertyService

property_service = PropertyService()


@app.route("/property", HttpMethod.POST)
def get_properties(request, body):
    return property_service.get_properties(**body)
