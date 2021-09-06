from django.shortcuts import redirect
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from qleader.models import Result
import qleader.fci.fci_H2 as fci


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def leaderboard(request, *args, **kwargs):
    result_list = kwargs.get("result_list", None)
    criterion = kwargs.get("criterion", None)
    if criterion == "closest_minimum":
        list_name = "Closest minimum energy distances to \"FCI def2_QZVPPD\" minimum energy distance"
    elif criterion == "smallest_variance":
        list_name = "Smallest variances from \"FCI def2_QZVPPD\""
    elif not criterion:
        return redirect("/")
    else:
        list_name = "Minimum energies"
    return Response(
        {
            "results": result_list,
            "list_name": list_name,
            "criterion": criterion,
        },
        template_name="leaderboard.html",
    )


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def invoke_leaderboard(request, criterion):

    if criterion == "closest_minimum":
        result_list = list(Result.objects.all())
        true_bond_distance = fci.get_minimum_distance("def2-QZVPPD")
        result_list.sort(key=lambda x: x.min_energy_distance-true_bond_distance)
    elif criterion == "smallest_variance":
        result_list = Result.objects.filter(include_in_variance=True).order_by("variance_from_fci")[:10]
    else:
        criterion = "min_energy"
        result_list = Result.objects.order_by("min_energy")[:10]

    return leaderboard(request._request, result_list=result_list, criterion=criterion)
