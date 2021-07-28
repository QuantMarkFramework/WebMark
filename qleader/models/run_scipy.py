from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, TextField, FloatField, SmallIntegerField
from qleader.models.run import Run
from .result import Result


# An abstract class for scipy based
class RunScipy(Run):
    energy_evaluations = TextField(default="")
    angles_evaluations = TextField(default="")
    fun = FloatField(default=None)
    message = TextField(default="")
    status = SmallIntegerField(default=None)
    success = CharField(default="", max_length=20)
    x = TextField(default="")

    class Meta:
        abstract = True


# "Nelder-Mead" optimizer
class RunScipyNelderMead(RunScipy):
    result = models.ForeignKey(
        Result, related_name='runs_nelder_mead', on_delete=CASCADE
        )  # Must be here!
    hessians = TextField(default="", blank=True)
    final_simplex = TextField(default="")
    nfev = SmallIntegerField(default=None, blank=True, null=True)
    nit = SmallIntegerField(default=None)


# "BFGS" optimizer
class RunScipyBFGS(RunScipy):
    result = models.ForeignKey(Result, related_name='runs_bfgs', on_delete=CASCADE)  # Must be here!
    gradients_evaluations = TextField(default="")
    jac = TextField(default="", blank=True)
    hess_inv = TextField(default="", blank=True)
    hessians = TextField(default="", blank=True)
    nfev = SmallIntegerField(default=None, blank=True, null=True)
    nit = SmallIntegerField(default=None)
    njev = SmallIntegerField(default=None, blank=True, null=True)


# "L-BFGS-B" optimizer !!! Could be the same class than BFGS at the moment ^ !!!
class RunScipyLBFGSB(RunScipy):
    result = models.ForeignKey(Result, related_name='runs_lbfgsb', on_delete=CASCADE)  # Must be here!
    gradients_evaluations = TextField(default="")
    jac = TextField(default="", blank=True)
    hess_inv = TextField(default="", blank=True)
    hessians = TextField(default="", blank=True)
    nfev = SmallIntegerField(default=None, blank=True, null=True)
    nit = SmallIntegerField(default=None)
    njev = SmallIntegerField(default=None, blank=True, null=True)


# "COBYLA" optimizer
class RunScipyCOBYLA(RunScipy):
    result = models.ForeignKey(Result, related_name='runs_cobyla', on_delete=CASCADE)  # Must be here!
    hessians = TextField(default="", blank=True)
    nfev = SmallIntegerField(default=None, blank=True, null=True)
    maxcv = FloatField(default=None)
