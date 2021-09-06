from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_token(request):
    user = request.user
    token = Token.objects.get(user=user)
    return Response({'Token': f'{token}'}, status=status.HTTP_200_OK)
