import ast
from qleader.models.result import Result
from qleader.models.run_scipy import RunScipyNelderMead, RunScipyBFGS, RunScipyLBFGSB, RunScipyCOBYLA


def create_result(dict):
    try:
        keys = ["tqversion", "optimizer", "basis_set", "transformation"]
        result_dict = {key: dict[key] for key in keys}
        result = Result(**result_dict)
        result.save()
        runs_all = create_runs(result, dict)
        lowest_energy = float("inf")
        for run in runs_all:
            if run.energy < lowest_energy:
                lowest_energy = run.energy
            run.save()
        result.min_energy = lowest_energy
        result.save()
        return "NoErr"
    except Exception as e1:
        try:
            result.delete()
        except Exception as e2:
            return str(e2)
        return str(e1)


def create_runs(result, data):
    sep_data = [{"energy": e} for e in data["energies"]]
    for i, entry in enumerate(sep_data):
        entry["variables"] = get_variables(data, i)
        entry["hamiltonian"] = get_hamiltonian(data, i)
        entry["ansatz"] = get_ansatz(data, i)
        entry["molecule"] = get_molecule(data, i)
        entry["distance"] = get_distance(data, i)
        entry.update(get_history(data, i))
        entry.update(get_scipy_results(data, i))
    runs = create_runs_based_on_optimizer(result, sep_data)
    return runs

# Select correct class depending on the optimizer used.
def create_runs_based_on_optimizer(result, sep_data):
    if result.get_optimizer().lower() == "nelder-mead":
        return [RunScipyNelderMead(result=result, **entry) for entry in sep_data]
    elif result.get_optimizer().lower() == "bfgs":
        return [RunScipyBFGS(result=result, **entry) for entry in sep_data]
    elif result.get_optimizer().lower() == "l-bfgs-b":
        return [RunScipyLBFGSB(result=result, **entry) for entry in sep_data]
    elif result.get_optimizer().lower() == "cobyla":
        return [RunScipyCOBYLA(result=result, **entry) for entry in sep_data]


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
