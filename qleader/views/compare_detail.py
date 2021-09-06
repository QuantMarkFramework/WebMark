from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from qleader.models import Result
import qleader.fci.fci_H2 as fci
import qleader.hf.hf_H2 as hf


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def compare_detail(request):
    result_ids = request.GET.getlist('id[]')
    results = Result.objects.filter(id__in=result_ids)
    run_list = [result.get_runs() for result in results]

    distances = [[results.distance for results in run] for run in run_list]
    energies = [[results.energy for results in run] for run in run_list]

    fci_distances, fci_energies = zip(*fci.get_fci("def2-QZVPPD"))

    names = ["_".join([result.basis_set, result.transformation, result.optimizer]) for result in results]
    ids = [result.id for result in results]
    identifiers = [[ids[i], names[i]] for i in range(len(ids))]

    # Only start gathering information for the error vs ciruit depth chart
    # if all basis_sets are the same.
    basis_sets = [result.basis_set for result in results]
    equivalent = "false"
    ground_truth, experiment_approx, experiment_truth, depths, min_energies = (0,)*5
    if basis_sets.count(basis_sets[0]) == len(basis_sets):
        # bond_distance = fci.get_minimum_distance("def2-QZVPPD")
        # FIXME bond_distance might not be available in the results. Hardcode 0.70 for now.
        bond_distance = 0.70
        ground_truth = fci.get_fci_value_by_dist("def2-QZVPPD", bond_distance)
        experiment_truth = fci.get_fci_value_by_dist(basis_sets[0], bond_distance)
        experiment_approx = hf.get_hf_value_by_dist(basis_sets[0], bond_distance)
        equivalent = "true"
        # For now we can assume that all runs have the same gate depths.
        depths = [result.get_runs()[0].fermionic_depth for result in results]
        # FIXME Different runs might have min_energy at different distances
        # and some might lack a value for the 'real' bond_distance
        min_energies = [result.min_energy for result in results]

    return Response(
        {
            "equivalent": equivalent,
            "data": [
                identifiers,
                results[0].basis_set,
                energies,
                distances,
                list(fci_distances),
                list(fci_energies),
                ground_truth,
                experiment_truth,
                experiment_approx,
                depths,
                min_energies,
            ]
        },
        template_name='compare_detail.html'
    )
