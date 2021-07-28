import pytest
import qleader.fci.fci_H2 as fci
from qleader.fci.fci_basis_sets_H2 import sto_3g, six_31g, def2_QZVPPD


# Test that get_fci returns sto_3g tuple when argument is "sto_3g"
def test_get_fci_basis_set_sto_3g():
    assert fci.get_fci("sto-3g") == [tuple(item) for item in sto_3g.items()]


# Test that get_fci returns six_31g tuple when argument is "6-31g"
def test_get_fci_basis_set_six_31g():
    assert fci.get_fci("6-31g") == [tuple(item) for item in six_31g.items()]


# Test that get_fci returns def2_QZVPPD tuple when argument is "def2-QZVPPD"
def test_get_fci_basis_set_def2_QZVPPD():
    assert fci.get_fci("def2-QZVPPD") == [tuple(item) for item in def2_QZVPPD.items()]


# Test that if the given basis set is unknown then get_fci rises ValueError.
def test_get_fci_rises_value_error_if_unknown_basis_set():
    with pytest.raises(ValueError):
        fci.get_fci("abc-123")


# Test that fci values for 'sto-3g' with given distance
# (which has a value) the value is correct (test couple examples).
def test_get_fci_value_by_dist_sto_3g_in_keys():
    assert fci.get_fci_value_by_dist("sto-3g", 0.1) == 2.7099607683997657
    assert fci.get_fci_value_by_dist("sto-3g", 2.10) == -0.9443746810834238
    assert fci.get_fci_value_by_dist("sto-3g", 3.0) == -0.9336318445559841


# Test that fci values for 'sto-3g' with given distance
# (which has not a value for that distance) the value is correctly
# estimated by interpolating (test couple examples).
def test_get_fci_value_by_dist_sto_3g_out_of_keys():
    assert fci.get_fci_value_by_dist("sto-3g", 0.09) == 2.7099607683997657
    assert fci.get_fci_value_by_dist("sto-3g", 2.11) == -0.9440596163416164
    assert fci.get_fci_value_by_dist("sto-3g", 3.04) == -0.9336318445559841


# Test that fci values for '6-31g' with given distance
# (which has a value) the value is correct (test couple examples).
def test_get_fci_value_by_dist_six_31g_in_keys():
    assert fci.get_fci_value_by_dist("6-31g", 0.1) == 2.57108876461466
    assert fci.get_fci_value_by_dist("6-31g", 2.10) == -1.0100960837563022
    assert fci.get_fci_value_by_dist("6-31g", 3.0) == -0.9974548288640583


# Test that fci values for '6-31g' with given distance
# (which has not a value for that distance) the value is correctly
# estimated by interpolating (test couple examples).
def test_get_fci_value_by_dist_six_31g_out_of_keys():
    assert fci.get_fci_value_by_dist("6-31g", 0.09) == 2.57108876461466
    assert fci.get_fci_value_by_dist("6-31g", 2.11) == -1.0097658403939274
    assert fci.get_fci_value_by_dist("6-31g", 3.04) == -0.9974548288640583


# Test that fci values for 'def2-QZVPPD' with given distance
# (which has a value) the value is correct (test couple examples).
def test_get_fci_value_by_dist_def2_QZVPPD_in_keys():
    assert fci.get_fci_value_by_dist("def2-QZVPPD", 0.1) == 2.483228142870508
    assert fci.get_fci_value_by_dist("def2-QZVPPD", 2.10) == -1.0166440148270257
    assert fci.get_fci_value_by_dist("def2-QZVPPD", 3.0) == -1.0012192081020863


# Test that fci values for 'def2-QZVPPD' with given distance
# (which has not a value for that distance) the value is correctly
# estimated by interpolating (test couple examples).
def test_get_fci_value_by_dist_def2_QZVPPD_out_of_keys():
    assert fci.get_fci_value_by_dist("def2-QZVPPD", 0.09) == 2.483228142870508
    assert fci.get_fci_value_by_dist("def2-QZVPPD", 2.11) == -1.0162253867149382
    assert fci.get_fci_value_by_dist("def2-QZVPPD", 3.04) == -1.0012192081020863


def test_get_fci_value_by_dist_rises_exception_if_unknown_basis_set():
    with pytest.raises(Exception):
        fci.get_fci_value_by_dist("abc-123", 0.1)


def test_get_fci_value_by_dist_rises_exception_if_error_occurs_in_try():
    with pytest.raises(Exception):
        fci.get_fci_value_by_dist("sto-3g", "1")  # E.g. TypeError (distance given as string)


def test_interpolate_gives_correct_value():
    assert fci.__interpolate(sto_3g, 0.3) == -0.6018037114169326
