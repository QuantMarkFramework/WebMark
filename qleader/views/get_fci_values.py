from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import qleader.fci.fci_H2 as fci


@api_view(["GET"])
def get_fci_values(request, basis_set):
    try:
        fci_values = fci.get_fci(basis_set)
        return Response(fci_values, status=status.HTTP_200_OK)
    except ValueError:
        return Response(status=status.HTTP_404_NOT_FOUND)
