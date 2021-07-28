import json
from rest_framework import status
from rest_framework.test import APITransactionTestCase
from qleader.tests.data_handler import post_data, scipy_examples, gradient_examples


# The test class for views.py.
class ViewsTests(APITransactionTestCase):
    def test_result_list_GET(self):
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_result_list_POST_valid_call(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_result_list_POST_invalid_call(self):
        response = post_data(self, json.dumps([]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_home_GET(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 0)
        post_data(self, scipy_examples["NELDER-MEAD"])
        response = self.client.get("")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 1)
        self.assertEqual(response.data["results"][0]["optimizer"], "NELDER-MEAD")

    def test_detail_GET(self):
        response = post_data(self, scipy_examples["NELDER-MEAD"])
        response = self.client.get("/api/" + str(response.data) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leaderboard_GET(self):
        response = self.client.get("/leaderboard/")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_invoke_leaderboard_closest_minimum(self):
        post_data(self, scipy_examples["NELDER-MEAD"])
        post_data(self, scipy_examples["BFGS"])
        post_data(self, gradient_examples["NESTEROV"])
        response = self.client.get("/leaderboard/closest_minimum/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 3)
        self.assertEqual(response.data["criterion"], "closest_minimum")
        self.assertEqual(response.data["results"][0].get_optimizer(), "NELDER-MEAD")
        self.assertEqual(response.data["results"][1].get_optimizer(), "BFGS")
        self.assertEqual(response.data["results"][2].get_optimizer(), "NESTEROV")

    def test_invoke_leaderboard_smallest_variance(self):
        post_data(self, scipy_examples["NELDER-MEAD"])
        post_data(self, scipy_examples["BFGS"])
        post_data(self, gradient_examples["NESTEROV"])
        response = self.client.get("/leaderboard/smallest_variance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 3)
        self.assertEqual(response.data["criterion"], "smallest_variance")
        self.assertEqual(response.data["results"][0].get_optimizer(), "NELDER-MEAD")
        self.assertEqual(response.data["results"][1].get_optimizer(), "BFGS")
        self.assertEqual(response.data["results"][2].get_optimizer(), "NESTEROV")

    def test_invoke_leaderboard_min_energy(self):
        post_data(self, scipy_examples["NELDER-MEAD"])
        post_data(self, scipy_examples["BFGS"])
        post_data(self, gradient_examples["NESTEROV"])
        response = self.client.get("/leaderboard/min_energy/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) == 3)
        self.assertEqual(response.data["criterion"], "min_energy")
        self.assertEqual(response.data["results"][0].get_optimizer(), "NESTEROV")
        self.assertEqual(response.data["results"][1].get_optimizer(), "BFGS")
        self.assertEqual(response.data["results"][2].get_optimizer(), "NELDER-MEAD")
