from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from qleader.models import Result


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def home(request):

    if request.method == "GET":
        results = Result.objects.all().order_by("created")

        # make own_results
        if (request.user.id is not None):
            token = Token.objects.get(user=request.user)
            own_results = results.filter(user=Token.objects.get(key=str(token)).user)
        else:
            own_results = results.filter(user=None)

        # filter results to only include own results and public other results
        filtered_results = results.filter(public=True).union(own_results)

        return Response(
            {
                "results": filtered_results.values(
                    'id',
                    'basis_set',
                    'transformation',
                    'optimizer',
                    'created',
                    'user__username'
                ),
                "own_results": own_results.values(),
            },
            template_name="home.html",
        )
