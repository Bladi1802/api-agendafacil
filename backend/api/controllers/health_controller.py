from rest_framework.response import Response
from rest_framework import status

def health_check(request):
    return Response(
        {"status": "ok", "project": "AgendaFacil"},
        status=status.HTTP_200_OK
    )
