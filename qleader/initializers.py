import ast
import math
from qleader.models.result import Result
from qleader.models.run_gradient import RunGradient
from qleader.models.run_scipy import RunScipyNelderMead, RunScipyBFGS, RunScipyLBFGSB, RunScipyCOBYLA
from qleader.fci.fci_H2 import get_fci_value_by_dist
from qleader.models.optimizers import gradient_optimizers, scipy_optimizers
import numpy as np


def create_result(dict, user):
    try:
        keys = ["tqversion", "optimizer", "basis_set", "transformation"]
        result_dict = {key: dict[key] for key in keys}
        result = Result(user=user, **result_dict)
        result.save()
        runs_all = create_runs(result, dict, dict["optimizer"])

        result.molecule = get_molecule(dict, 0)
        result.atoms = get_atoms(dict, 0)
        result.min_energy, result.min_energy_distance, \
            result.min_energy_qubits = get_lowest_energy(runs_all)
        result.variance_from_fci = get_variance(runs_all)
        result.include_in_variance = check_distances(runs_all)

        for run in runs_all:
            run.save()

        result.save()
        return result
    except Exception as error:
        print(f'Exception in initializers.py: {repr(error)}')
        result.delete()


def add_extra_fields(sep_data, data, optimizer):
    if optimizer.upper() in scipy_optimizers:
        for i, entry in enumerate(sep_data):
            entry.update(get_scipy_results(data, i))
    elif optimizer.upper() in gradient_optimizers:
        for i, entry in enumerate(sep_data):
            entry.update(get_moments(data, i))
    return sep_data


def create_runs(result, data, optimizer):
    sep_data = [{"energy": e} for e in data["energies"]]
    for i, entry in enumerate(sep_data):
        entry["variables"] = data["variables"][i]
        entry["hamiltonian"] = data["hamiltonian"][i]
        entry["ansatz"] = data["ansatz"][i]
        entry["distance"] = get_distance(data, i)
        entry["qubits"] = data["qubits"][i]
        entry["elementary_depth"] = data["elementary_depth"][i]
        entry["fermionic_depth"] = data["fermionic_depth"][i]
        entry["single_qubit_gates"] = data["single_qubit"][i]
        entry["double_qubit_gates"] = data["double_qubit"][i]
        entry.update(get_history(data, i))
    sep_data = add_extra_fields(sep_data, data, optimizer)
    runs = create_runs_based_on_optimizer(result, sep_data)
    return runs


# Select correct class depending on the optimizer used.
def create_runs_based_on_optimizer(result, sep_data):
    if result.get_optimizer().upper() == "NELDER-MEAD":
        return [RunScipyNelderMead(result=result, **entry) for entry in sep_data]
    elif result.get_optimizer().upper() == "BFGS":
        return [RunScipyBFGS(result=result, **entry) for entry in sep_data]
    elif result.get_optimizer().upper() == "L-BFGS-B":
        return [RunScipyLBFGSB(result=result, **entry) for entry in sep_data]
    elif result.get_optimizer().upper() == "COBYLA":
        return [RunScipyCOBYLA(result=result, **entry) for entry in sep_data]
    elif result.get_optimizer().upper() in gradient_optimizers:
        return [RunGradient(result=result, **entry) for entry in sep_data]
    else:
        raise ValueError(f'Unknown optimizer {result.get_optimer()}')


def get_lowest_energy(runs_all):
    lresult = min(runs_all, key=lambda x: x.energy)
    return lresult.energy, lresult.distance, lresult.qubits


def get_variance(runs_all):
    return np.var(
        [r.energy - get_fci_value_by_dist("def2-QZVPPD", r.distance) for r in runs_all]
    )


def get_molecule(data, i):
    return data["molecule"][i]


def get_distance(data, i):
    coordinates = [mole[1] for mole in data["geometries"][i]]
    pairs = zip(coordinates[0], coordinates[1])
    d = math.sqrt(sum([(c[0] - c[1])**2 for c in pairs]))
    return d


def get_atoms(data, i):
    return [mole[0] for mole in data["geometries"][i]]


def get_history(data, i):
    history_dict = {
        str(key): str(val)
        for key, val in ast.literal_eval(data["histories"][i]).items()
    }
    return history_dict


def get_scipy_results(data, i):
    return ast.literal_eval(data["scipy_results"][i])


def get_moments(data, i):
    return {"moments": data["moments"][i]}


def check_distances(data):
    distances = sorted([round(r.distance, 2) for r in data])
    lb_distances = [round(x, 2) for x in np.linspace(0.1, 2, 20)]
    if len(distances) != len(lb_distances):
        return False
    for d in zip(distances, lb_distances):
        if d[0] != d[1]:
            return False
    return True
