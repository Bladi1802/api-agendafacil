from rest_framework.response import Response
from rest_framework import status

# Mock en memoria (sin base de datos)
SERVICES = [
    {"id": 1, "name": "Corte", "duration_minutes": 30, "price": 150.00},
    {"id": 2, "name": "Afinación", "duration_minutes": 60, "price": 800.00},
]

def list_services(request):
    return Response(SERVICES, status=status.HTTP_200_OK)

def create_service(request):
    data = request.data or {}

    name = data.get("name")
    duration = data.get("duration_minutes")
    price = data.get("price")

    # Validación mínima
    if not name or duration is None or price is None:
        return Response(
            {"error": "Campos requeridos: name, duration_minutes, price"},
            status=status.HTTP_400_BAD_REQUEST
        )

    new_id = (max([s["id"] for s in SERVICES]) + 1) if SERVICES else 1

    new_service = {
        "id": new_id,
        "name": str(name),
        "duration_minutes": int(duration),
        "price": float(price),
    }

    SERVICES.append(new_service)
    return Response(new_service, status=status.HTTP_201_CREATED)
