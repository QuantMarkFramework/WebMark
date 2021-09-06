import numpy as np
from qleader.hf.hf_basis_sets_H2 import sto_3g, six_31g, def2_QZVPPD


def get_hf(basis_set):
    if basis_set == "sto-3g":
        items = sto_3g.items()
    elif basis_set == "6-31g":
        items = six_31g.items()
    elif basis_set == "def2-QZVPPD":
        items = def2_QZVPPD.items()
    else:
        raise ValueError("Basis set was not one of the supported ones (6-31g, sto-3g or def2_QZVPPD)")

    return [tuple(item) for item in items]


def get_minimum_distance(basis_set):
    if basis_set == "sto-3g":
        items = sto_3g.items()
    elif basis_set == "6-31g":
        items = six_31g.items()
    elif basis_set == "def2-QZVPPD":
        items = def2_QZVPPD.items()
    else:
        raise ValueError("Basis set was not one of the supported ones (6-31g, sto-3g or def2_QZVPPD)")
    return min(items, key=lambda x: x[1])[0]


def get_hf_value_by_dist(basis_set, distance):
    """Get Hartree-Fock values for H2

    basis_set: sto-3g, 6-31g or def2_QZVPPD
    distance: float between [0.1, 3.0]
    """
    try:
        # Round to one because the actual distances might vary a little because of the psi4 issue.
        distance = round(distance, 1)
        if basis_set == "sto-3g":
            if distance in sto_3g.keys():
                return sto_3g[distance]
            else:
                return __interpolate(sto_3g, distance)
        elif basis_set == "6-31g":
            if distance in six_31g.keys():
                return six_31g[distance]
            else:
                return __interpolate(six_31g, distance)
        elif basis_set == "def2-QZVPPD":
            if distance in def2_QZVPPD.keys():
                return def2_QZVPPD[distance]
            else:
                return __interpolate(def2_QZVPPD, distance)
        else:
            return __interpolate(basis_set, distance)
    except Exception as e:
        raise Exception(str(e))


def __interpolate(basis_set, distance):

    xp = list(basis_set.keys())
    fp = list(basis_set.values())

    return np.interp(distance, xp, fp)
