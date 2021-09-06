from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from qleader.models import Result
from django.contrib.auth.models import User


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def profile(request, user_id):

    try:
        user = User.objects.get(id=user_id)
    except Exception:  # TODO: fallback not working correctly at the moment
        return Response(status=status.HTTP_404_NOT_FOUND)

    # make own_results
    results = Result.objects.all().order_by("created")
    if (request.user.id is user_id):
        profile_results = results.filter(user=request.user)
    else:
        profile_results = results.filter(public=True)
        profile_results = profile_results.filter(user=user)

    return Response(
        {
            "profile_user": user,
            "profile_results": profile_results,
        },
        template_name="profile.html",
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def modify_profile(request, user_id):

    if request.method != "POST":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    user = User.objects.get(id=user_id)

    if request.user == user:
        user.userprofile.real_name = request.data['realName']
        user.userprofile.institution = request.data['institution']
        user.userprofile.bio = request.data['bio']
        user.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
