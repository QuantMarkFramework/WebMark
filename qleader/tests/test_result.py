from rest_framework.test import APITransactionTestCase
from qleader.tests.data_handler import post_data, examples
from qleader.models.result import Result
from django.contrib.auth.models import User


# The test class for Result's custom methods
class ResultsTests(APITransactionTestCase):

    def setup_method(self, method):
        self.user, self.created = User.objects.get_or_create(username='Testi-Teppo')

    def test_get_optimizer(self):
        for optimizer, data in examples:
            response = post_data(self, data)
            result_id = response.data['result_id']
            result = Result.objects.get(id=result_id)
            self.assertTrue(optimizer == result.get_optimizer())

    def test_get_runs(self):
        for optimizer, data in examples:
            response = post_data(self, data)
            result_id = response.data['result_id']
            result = Result.objects.get(id=result_id)
            self.assertTrue(15 == len(result.get_runs()))
            for run in result.get_runs():
                self.assertEqual(result_id, run.result.id)
