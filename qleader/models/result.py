from django.db import models
from django.db.models.fields import CharField, SmallIntegerField, TextField, FloatField
from qleader.models.optimizers import gradient_optimizers


class Result(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    optimizer = CharField(default="", max_length=50)
    tqversion = TextField(default="")
    basis_set = CharField(default="", max_length=50)
    transformation = CharField(default="", max_length=50)
    min_energy = FloatField(default=float("inf"))
    min_energy_distance = FloatField(default=float("inf"))
    min_energy_qubits = SmallIntegerField(default=0)
    variance_from_fci = FloatField(default=float("inf"))

    def __str__(self):
        return str(self.id)

    def get_optimizer(self):
        return self.optimizer

    def get_runs(self):
        # Scipy
        if self.optimizer.upper() == "NELDER-MEAD":
            return self.runs_nelder_mead.order_by('distance')
        elif self.optimizer.upper() == "BFGS":
            return self.runs_bfgs.order_by('distance')
        elif self.optimizer.upper() == "L-BFGS-B":
            return self.runs_lbfgsb.order_by('distance')
        elif self.optimizer.upper() == "COBYLA":
            return self.runs_cobyla.order_by('distance')
        # Gradient
        elif self.optimizer.upper() in gradient_optimizers:
            return self.runs_gradient.order_by('distance')
