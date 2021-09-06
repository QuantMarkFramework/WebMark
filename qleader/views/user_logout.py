from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return redirect("/")
