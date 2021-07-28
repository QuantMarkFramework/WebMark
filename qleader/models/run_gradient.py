from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import TextField
from qleader.models.run import Run
from .result import Result


class RunGradient(Run):
    result = models.ForeignKey(
        Result, related_name='runs_gradient', on_delete=CASCADE
    )
    moments = TextField(default="", blank=True)
