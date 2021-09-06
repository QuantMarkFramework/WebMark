from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from qleader.models import Result


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def change_publicity(request, result_id):
    try:
        result = Result.objects.get(id=result_id)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif request.method == "POST":
        if result.user == request.user:
            result.public = request.data['boolean']
            result.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
