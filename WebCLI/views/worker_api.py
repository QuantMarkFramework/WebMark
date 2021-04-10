from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Metrics, Average_history, Accuracy_history
from django.utils import timezone
import json


def as_analyzed_results(result):
    metrics = Metrics.objects.get(pk=result["metrics_id"])
    metrics.qubit_count = result["qubit_count"]
    metrics.timestamp = timezone.now()
    metrics.gate_depth = result["gate_depth"]
    metrics.average_iterations = result["average_iterations"]
    metrics.success_rate = result["success_rate"]
    return metrics


def as_average_history(result):
    histories = result["average_history"]
    existing_avg_history = Average_history.objects.filter(analyzed_results=result["metrics_id"])
    if len(existing_avg_history) > 0:
        return existing_avg_history[0]
    else:
        for i in range(len(histories)):
            average_history = Average_history(
                analyzed_results=Metrics.objects.get(pk=result["metrics_id"]),
                data=histories[i],
                iteration_number=i+1)
            average_history.save()
        return average_history


def as_accuracy_history(result):
    histories = result["accuracy_history"]
    existing_acc_history = Accuracy_history.objects.filter(analyzed_results=result["metrics_id"])
    if len(existing_acc_history) > 0:
        return existing_acc_history[0]
    else:
        for i in range(len(histories)):
            accuracy_history = Accuracy_history(
                analyzed_results=Metrics.objects.get(pk=result["metrics_id"]),
                data=histories[i],
                iteration_number=i+1)
            accuracy_history.save()
    return accuracy_history


# TODO: set this route to accept from workers only
@csrf_exempt
def handle_result(request):
    analyzed_results = json.loads(request.POST["data"], object_hook=as_analyzed_results)
    analyzed_results.save()
    avg_history_results = json.loads(request.POST["data"], object_hook=as_average_history)
    avg_history_results.save()
    avg_accuracy_results = json.loads(request.POST["data"], object_hook=as_accuracy_history)
    avg_accuracy_results.save()
    return HttpResponse("ok")
