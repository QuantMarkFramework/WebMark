from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from qleader.models import Result


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_result(request, result_id, type):
    result = Result.objects.get(id=result_id)

    if result.public is False and result.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if type == "dump":
        res = result.get_dump()
    elif type == "experiment":
        res = result.get_experiment()

    return Response(res, status=status.HTTP_200_OK)
