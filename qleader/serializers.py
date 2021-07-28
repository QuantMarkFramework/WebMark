from rest_framework import serializers
from qleader.models import Run


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = ['id', 'created', 'energy', 'optimizer', 'tqversion', 'variables',
                  'history_energies', 'gradients', 'angles', 'energies_calls', 'gradients_calls',
                  'angles_calls', 'final_simplex', 'fun', 'message', 'nfev', 'nit', 'status',
                  'success', 'x', 'hamiltonian', 'ansatz', 'molecule', 'distance']
