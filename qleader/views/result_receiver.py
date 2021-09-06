from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from qleader.initializers import create_result
import json


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def result_receiver(request):

    if request.method == "GET":
        return Response()
    elif request.method == "POST":
        data_dict = json.loads(request.data)
        user = request.user
        try:
            result = create_result(data_dict, user)
            return Response({'message': 'Success', 'result_id': result.id},
                            status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_400_BAD_REQUEST)
