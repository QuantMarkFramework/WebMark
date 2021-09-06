import ast
import json
import qleader.initializers as initializers
from rest_framework.test import APITransactionTestCase
from qleader.tests.data_handler import (post_data_all_examples, get_home, scipy_examples,
                                        gradient_examples, special_examples)
from rest_framework.test import force_authenticate, APIRequestFactory
from django.contrib.auth.models import User
from qleader import views


# The test class for testing the initializers.py
# The class uses DRF's APITransactionTestCase that
# has tools for testing and it provides data handling
# while testing. See the documentation at
# https://www.django-rest-framework.org/api-guide/testing
class InitializersTests(APITransactionTestCase):

    def setup_method(self, method):
        self.factory = APIRequestFactory()
        self.user, self.created = User.objects.get_or_create(username='Testi-Teppo')

    # Test that Result object has correct fields after creation.
    def test_creating_results_based_on_examples(self):
        post_data_all_examples(self)
        response = get_home(self, self.user)

        n = len(response.data["results"])
        assert n == len(scipy_examples) + len(gradient_examples)
        for i in range(0, n):
            # Find the specific Result based on id in the query data
            result_id = response.data["results"][i]["id"]
            request = self.factory.get("/api/" + str(result_id) + "/")
            view = views.detail
            force_authenticate(request, user=self.user)
            result = view(request, result_id=result_id).data["result"]

            # Check that every field is not its default value. This indicates that the Result
            # has that field and there is data in it.
            assert result.created is not None
            assert result.optimizer, result.tqversion != ""
            assert result.basis_set, result.transformation != ""
            assert result.molecule != ""
            assert result.min_energy, result.min_energy_distance != float("inf")
            assert result.variance_from_fci != float("inf")
            assert result.min_energy_qubits != 0

    # A helper method to clear the 'test_created_results_have_correct_runs'
    def assert_Run_fields_similar_to_all(self, runs):
        for run in runs:
            assert run.distance, run.energy is not None
            assert run.elementary_depth != 0
            fields_should_be_unempty = [run.variables, run.energies, run.gradients, run.angles,
                                        run.energies_calls, run.gradients_calls, run.angles_calls,
                                        run.hamiltonian, run.ansatz, run.qubits]
            for field in fields_should_be_unempty:
                assert field != ""

    # A helper method to clear the 'test_created_results_have_correct_runs'
    def assert_Run_fields_similar_to_scipy_based(self, runs):
        for run in runs:
            assert run.fun, run.status is not None
            fields_should_be_unempty = [run.energy_evaluations, run.x,
                                        run.angles_evaluations, run.message, run.success]
            for field in fields_should_be_unempty:
                assert field != ""

    # A helper method to clear the 'test_created_results_have_correct_runs'
    def assert_Run_fields_similar_to_NELDER_MEAD(self, runs):
        for run in runs:
            assert run.hessians, run.final_simplex != ""
            assert run.nfev, run.nit is not None

    # A helper method to clear the 'test_created_results_have_correct_runs'
    def assert_Run_fields_similar_to_BFGS(self, runs):
        for run in runs:
            assert run.jac, run.hess_inv != ""
            assert run.hessians, run.gradients_evaluations != ""
            assert run.nfev, run.nit is not None
            assert run.njev is not None

    # A helper method to clear the 'test_created_results_have_correct_runs'
    def assert_Run_fields_similas_to_COBYLA(self, runs):
        for run in runs:
            assert run.hessians != ""
            assert run.nfev, run.maxcv is not None

    # Test that the created Results have Runs with correct fields.
    # This method uses multiple helper methods to cut down its length
    # and to be more clear.
    def test_created_results_have_correct_runs(self):
        post_data_all_examples(self)
        response = get_home(self, self.user)
        n = len(response.data["results"])
        assert n == len(scipy_examples) + len(gradient_examples)
        for i in range(0, n):
            # Find the specific Result based on id in the query data
            result_id = response.data["results"][i]["id"]
            request = self.factory.get("/api/" + str(result_id) + "/")
            view = views.detail
            force_authenticate(request, user=self.user)
            response_detail = view(request, result_id=result_id)
            runs = response_detail.data["runs"]  # The Runs of the Result
            self.assert_Run_fields_similar_to_all(runs)
            # Get the optimizer of the Result
            optimizer = response.data["results"][i]["optimizer"]
            if optimizer in scipy_examples.keys():  # Runs have fields of RunScipy
                self.assert_Run_fields_similar_to_scipy_based(runs)
                if optimizer == "NELDER-MEAD":
                    self.assert_Run_fields_similar_to_NELDER_MEAD(runs)
                elif optimizer == "BFGS" or optimizer == "L-BFGS-B":
                    self.assert_Run_fields_similar_to_BFGS(runs)
                elif optimizer == "COBYLA":
                    self.assert_Run_fields_similas_to_COBYLA(runs)
            else:  # Runs have fields of RunGradient (the only field is moments).
                for run in runs:
                    assert run.moments != ""

    def test_get_history_returns_dict(self):
        history_dict = initializers.get_history(scipy_examples["NELDER-MEAD"], 0)
        assert type(history_dict) is dict

    def test_get_history_returns_energies(self):
        history_dict = initializers.get_history(scipy_examples["NELDER-MEAD"], 1)
        energy_list = ast.literal_eval(history_dict["energies"])
        assert energy_list[0] == 0.16417501091932965

    def test_get_hamiltonian(self):
        hamiltonian = scipy_examples["NELDER-MEAD"]["hamiltonian"][0]
        assert "+5.0607+0.3008Z(0)+0.3008Z(0)Z(1)-0.7265Z(2)" in hamiltonian

    def test_scipy_results_returns_dict(self):
        scipy_dict = initializers.get_scipy_results(scipy_examples["NELDER-MEAD"], 0)
        assert type(scipy_dict) is dict

    def test_scipy_results_for_nelder_mead(self):
        scipy_dict = initializers.get_scipy_results(scipy_examples["NELDER-MEAD"], 0)
        scipy_str = json.dumps(scipy_dict).replace('"', "'")
        example = "{'fun': '2.715887390825483', 'nit': '1', 'nfev': '2', 'status': '0', " + \
            "'success': 'True', 'message': 'Optimization terminated successfully.', 'x': '[0.]'," + \
            " 'final_simplex': '(array([[0.     ],\\n" + \
            "       [0.00025]]), array([2.71588739, 2.71596573]))'}"
        self.assertEqual(scipy_str, example)

    def test_scipy_results_for_bfgs(self):
        bfgs_dict = initializers.get_scipy_results(scipy_examples["BFGS"], 0)
        bfgs_str = json.dumps(bfgs_dict).replace('"', "'")
        example = "{'fun': '2.709960768402183', 'jac': '[-6.19888306e-06]', " + \
            "'hess_inv': '[[0.12144529]]', 'nfev': '4', 'njev': '4', 'status': '0', 'success': " + \
            "'True', 'message': 'Optimization terminated successfully.', " + \
            "'x': '[-0.03793231]', 'nit': '2'}"
        self.assertEqual(bfgs_str, example)

    def test_scipy_results_for_l_bfgs_b(self):
        l_bfgs_b_dict = initializers.get_scipy_results(scipy_examples["L-BFGS-B"], 0)
        l_bfgs_b_str = json.dumps(l_bfgs_b_dict).replace('"', "'")
        example = "{'fun': '2.709960768621836', 'jac': '[-6.00814819e-05]', " + \
            "'nfev': '4', 'njev': '4'," + \
            " 'nit': '2', 'status': '0', 'message': 'CONVERGENCE: " + \
            "NORM_OF_PROJECTED_GRADIENT_<=_PGTOL', " + \
            "'x': '[-0.03793889]', 'success': 'True', 'hess_inv': " + \
            "'<1x1 LbfgsInvHessProduct with dtype=float64>'}"
        self.assertEqual(l_bfgs_b_str, example)

    def test_scipy_results_for_cobyla(self):
        cobyla_dict = initializers.get_scipy_results(scipy_examples["COBYLA"], 0)
        cobyla_str = json.dumps(cobyla_dict).replace('"', "'")
        example = "{'x': '[-0.0370625]', 'status': '1', 'success': 'True', 'message': " + \
            "'Optimization terminated successfully.', 'nfev': '17', " + \
            "'fun': '2.709963880850985', 'maxcv': '0.0'}"
        self.assertEqual(cobyla_str, example)

    def test_get_moments_for_gradient_results_at_index(self):
        assert '[(array([0.]), array([0.39846589])),' in initializers.get_moments(
            gradient_examples["ADAGRAD"], 0)["moments"]
        assert '[(array([0.]), array([0.])), [array([0.03123407]),' in initializers.get_moments(
            gradient_examples["ADAM"], 0)['moments']
        assert '[(array([0.]), array([0.])), [array([0.03123407]),' in initializers.get_moments(
            gradient_examples["ADAMAX"], 0)['moments']
        assert '[(array([0.]), array([0.])), [array([-0.03123407]),' in initializers.get_moments(
            gradient_examples["MOMENTUM"], 0)['moments']
        assert '[(array([0.]), array([0.])), [array([-0.03123407]),' in initializers.get_moments(
            gradient_examples["NESTEROV"], 0)['moments']
        assert '[(array([0.02433759]), array([0.])),' in initializers.get_moments(
            gradient_examples["RMSPROP-NESTEROV"], 0)['moments']
        assert ', array([0.])), [array([0.]), array([9.75567356e-05])],' in initializers.get_moments(
            gradient_examples["RMSPROP"], 0)['moments']
        assert '[(array([0.]), array([0.])), (array([0.]),' in initializers.get_moments(
            gradient_examples["SGD"], 0)['moments']
        assert '[(array([0.]), array([0.])), (array([0.]),' in initializers.get_moments(
            gradient_examples["SPSA"], 0)['moments']

    def test_non_benchmark_distances_refused(self):
        result = initializers.create_result(scipy_examples["NELDER-MEAD"], self.user)
        assert not result.include_in_variance

    def test_benchmark_distances_accepted(self):
        result = initializers.create_result(special_examples["BENCHMARK_NELDER-MEAD"], self.user)
        assert result.include_in_variance
