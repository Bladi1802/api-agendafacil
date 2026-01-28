from django.urls import path
from rest_framework.decorators import api_view

from api.controllers.health_controller import health_check
from api.controllers.services_controller import list_services, create_service

@api_view(["GET", "POST"])
def services_handler(request):
    if request.method == "GET":
        return list_services(request)
    return create_service(request)

urlpatterns = [
    path("health/", api_view(["GET"])(health_check)),
    path("services/", services_handler),
]
