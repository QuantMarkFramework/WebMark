import ast
from qleader.models.result import Result
from qleader.models.run_gradient import RunGradient
from qleader.models.run_scipy import RunScipyNelderMead, RunScipyBFGS, RunScipyLBFGSB, RunScipyCOBYLA
from qleader.fci import get_fci_value_by_dist
from qleader.models.optimizers import gradient_optimizers
import numpy as np


def create_result(dict):
    try:
        keys = ["tqversion", "optimizer", "basis_set", "transformation"]
        result_dict = {key: dict[key] for key in keys}
        result = Result(**result_dict)
        result.save()
        runs_all = create_runs(result, dict, dict["optimizer"])

        result.min_energy, result.min_delta_distance = get_lowest_energy(runs_all)
        result.min_delta, result.min_delta_distance = get_lowest_delta(runs_all)
        result.variance_from_fci = get_variance(runs_all)

        for run in runs_all:
            run.save()

        result.save()
        return result
    except Exception as error:
        result.delete()
        raise Exception(f'Exception in initializers.py: {repr(error)}')


def add_extra_fields(sep_data, data, optimizer):
    if optimizer.upper() in ["NELDER-MEAD", "BFGS", "L-BFGS-B", "COBYLA"]:
        for i, entry in enumerate(sep_data):
            entry.update(get_scipy_results(data, i))
    elif optimizer.upper() in gradient_optimizers:
        for i, entry in enumerate(sep_data):
            entry.update(get_moments(data, i))
    return sep_data


def create_runs(result, data, optimizer):
    sep_data = [{"energy": e} for e in data["energies"]]
    for i, entry in enumerate(sep_data):
        entry["variables"] = get_variables(data, i)
        entry["hamiltonian"] = get_hamiltonian(data, i)
        entry["ansatz"] = get_ansatz(data, i)
        entry["molecule"] = get_molecule(data, i)
        entry["distance"] = get_distance(data, i)
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
    return lresult.energy, lresult.distance


def get_lowest_delta(runs_all):
    deltas = [(r, r.energy - get_fci_value_by_dist("def2-QZVPPD", r.distance)) for r in runs_all]
    ldresult = min(deltas, key=lambda x: x[1])
    return ldresult[1], ldresult[0].distance


def get_variance(runs_all):
    return np.var(
        [r.energy - get_fci_value_by_dist("def2-QZVPPD", r.distance) for r in runs_all]
    )


def get_variables(data, i):
    return data["variables"][i]


def get_hamiltonian(data, i):
    return data["hamiltonian"][i]


def get_ansatz(data, i):
    return data["ansatz"][i]


def get_molecule(data, i):
    return data["molecule"][i]


def get_distance(data, i):
    return data["distances"][i]


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
