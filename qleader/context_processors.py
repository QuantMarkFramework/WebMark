from django.conf import settings


def pass_path_prefix(request):
    return {
       'path_prefix': request.headers.get("SCRIPT_NAME", ""),
    }


def social_auth_services_status(request):
    return {
        'orcid_status': settings.ORCID_STATUS,
        'google_status': settings.GOOGLE_STATUS,
        'facebook_status': settings.FACEBOOK_STATUS
    }
