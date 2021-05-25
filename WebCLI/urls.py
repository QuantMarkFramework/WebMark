# pages/urls.py
from django.urls import path
from .views.new_algorithm import new_algorithm
from .views.new_molecule import new_molecule
from .views.new_algorithm_type import new_algorithm_type
from .views.view_molecule import view_molecule
from .views.new_version import add_version, load_methods
from .views.update_algorithm import update_algorithm
from .views.compare_algorithms import AlgorithmComparisonView
from .views.algorithm_details_view import AlgorithmDetailsView, in_analysis, refresh_metrics
from .views.homepage import AlgorithmListView
from .views.my_algorithms import MyAlgorithmListView
from .forms import SignUpView
from .views.worker_api import handle_result

urlpatterns = [
    path('', AlgorithmListView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('newAlgorithm/', new_algorithm, name='newAlgorithm'),
    path('newMolecule/', new_molecule, name='newMolecule'),
    path('newAlgorithmType/', new_algorithm_type, name='newAlgorithmType'),
    path('algorithm/<int:algorithm_id>', AlgorithmDetailsView.as_view(), name='algorithm_details'),
    path('myAlgorithms/', MyAlgorithmListView.as_view(), name="myAlgorithms"),
    path('compare/<int:a1_id>/<int:a2_id>',
         AlgorithmComparisonView.as_view(), name="compare_algorithms"),
    path('addVersion/', add_version, name='add_version'),
    path('updateAlgorithm/', update_algorithm, name='updateAlgorithm'),
    path('handleResult', handle_result),
    path('methods_of_module/', load_methods, name='load_methods'),
    path('molecule/<int:molecule_id>', view_molecule, name='viewMolecule'),
    path('in_analysis/', in_analysis, name='in_analysis'),
    path('metrics/', refresh_metrics, name='refresh_metrics'),
]
