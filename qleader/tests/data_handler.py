import os
import sys
import ast
import json
from rest_framework.test import force_authenticate, APIRequestFactory
from qleader import views

# To see how Django REST framework can be tested (and has been done in here)
# follow the link https://www.django-rest-framework.org/api-guide/testing


# Read a file located at the given path and return the json object from the file.
def create_test_data_from_example(path):
    return ast.literal_eval(
        open(os.path.join(sys.path[0], path), "r").read()
    )


# Send test data to API (".../api/") and return the response.
# More about DRF's API test cases is at
# https://www.django-rest-framework.org/api-guide/testing/#api-test-cases
def post_data(self, data):
    factory = APIRequestFactory()
    request = factory.post("/api/", data=json.dumps(data), format='json')
    view = views.result_receiver
    force_authenticate(request, user=self.user)
    response = view(request)

    return response


special_examples = {
    "BENCHMARK_NELDER-MEAD": create_test_data_from_example("tests/test_data/example_benchmark_NELDER-MEAD.txt"), # noqa
}

scipy_examples = {
    "NELDER-MEAD": create_test_data_from_example("tests/test_data/example_NELDER-MEAD.txt"),
    "BFGS": create_test_data_from_example("tests/test_data/example_BFGS.txt"),
    "L-BFGS-B": create_test_data_from_example("tests/test_data/example_L-BFGS-B.txt"),
    "COBYLA": create_test_data_from_example("tests/test_data/example_COBYLA.txt")
}

gradient_examples = {
    "ADAGRAD": create_test_data_from_example("tests/test_data/example_ADAGRAD.txt"),
    "ADAM": create_test_data_from_example("tests/test_data/example_ADAM.txt"),
    "ADAMAX": create_test_data_from_example("tests/test_data/example_ADAMAX.txt"),
    "MOMENTUM": create_test_data_from_example("tests/test_data/example_MOMENTUM.txt"),
    "NADAM": create_test_data_from_example("tests/test_data/example_NADAM.txt"),
    "NESTEROV": create_test_data_from_example("tests/test_data/example_NESTEROV.txt"),
    "RMSPROP-NESTEROV": create_test_data_from_example("tests/test_data/example_RMSPROP-NESTEROV.txt"),
    "RMSPROP": create_test_data_from_example("tests/test_data/example_RMSPROP.txt"),
    "SGD": create_test_data_from_example("tests/test_data/example_SGD.txt"),
    "SPSA": create_test_data_from_example("tests/test_data/example_SPSA.txt")
}


examples = []
[examples.append(item) for item in scipy_examples.items()]
[examples.append(item) for item in gradient_examples.items()]


# Calls the post_data method for all test examples
def post_data_all_examples(self):
    [post_data(self, data) for data in scipy_examples.values()]
    [post_data(self, data) for data in gradient_examples.values()]


# Helper method
def get_home(self, user):
    request = self.factory.get("")
    force_authenticate(request, user=user)
    view = views.home
    response = view(request)

    return response
