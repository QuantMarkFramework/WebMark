import ast
from django.db import models
from django.db.models.fields import TextField, FloatField, SmallIntegerField


class Run(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    distance = FloatField(default=None)
    energy = FloatField(default=None)
    variables = TextField(default="")
    energies = TextField(default="")
    gradients = TextField(default="")
    angles = TextField(default="")
    energies_calls = TextField(default="")
    gradients_calls = TextField(default="")
    angles_calls = TextField(default="")
    hamiltonian = TextField(default="")
    ansatz = TextField(default="")
    molecule = TextField(default="")
    qubits = SmallIntegerField(default=0)
    gate_depth = SmallIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['created']

    def get_iteration_energies(self):
        return ast.literal_eval(self.energies)
