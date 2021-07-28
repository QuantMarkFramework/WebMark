import os
import sys
import ast
import json

# To see how Django REST framework can be tested (and has been in here)
# follow the link https://www.django-rest-framework.org/api-guide/testing


# Read a file located at the given path and return the json object in the file.
def create_test_data_from_example(path):
    return ast.literal_eval(
        open(os.path.join(sys.path[0], path), "r").read()
    )


# Send test data to API (".../api/") and return the response.
# More about DRF's API test cases (which the 'self' should have)
# is at https://www.django-rest-framework.org/api-guide/testing/#api-test-cases
def post_data(self, data):
    response = self.client.post("/api/", data=json.dumps(data), format='json')
    return response


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
    for data in scipy_examples.values():
        post_data(self, data)
    for data in gradient_examples.values():
        post_data(self, data)
