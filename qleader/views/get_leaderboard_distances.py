from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np


@api_view(["GET"])
def get_leaderboard_distances(request):
    if request.method == "GET":
        distances = [round(x, 2) for x in np.linspace(0.1, 2, 20)]
        return Response(distances, status=status.HTTP_200_OK)
