from django.db import models
from django.db.models.fields import (BooleanField, CharField, SmallIntegerField,
                                     TextField, FloatField, URLField)
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
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
    include_in_variance = BooleanField(default=False)
    user = models.ForeignKey(
        User, related_name='result_user', on_delete=CASCADE, default=None
    )
    public = BooleanField(default=False)
    info = TextField(default="")
    molecule = TextField(default="")
    atoms = TextField(default="")
    github_link = URLField(default="")
    article_link = URLField(default="")

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

    def get_dump(self):
        result_dict = self.__dict__
        runs = [r.__dict__ for r in self.get_runs()]
        for r in runs:
            del r['_state']
            del r['created']
        del result_dict['user_id']
        del result_dict['public']
        del result_dict['_state']
        result_dict['created'] = str(result_dict['created'])
        result_dict.update({'runs': runs})
        return result_dict

    def get_experiment(self):
        return {'distances': [r.distance for r in self.get_runs()],
                'ansatz': [r.ansatz for r in self.get_runs()],
                'transformation': self.transformation,
                'basis_set': self.basis_set,
                'optimizer': self.optimizer}
