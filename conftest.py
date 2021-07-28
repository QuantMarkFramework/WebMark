import os
import django
from django.conf import settings

# Note to devs: this file with its commentary is modified from the instructions published here:
# http://engineroom.trackmaven.com/blog/using-pytest-with-django/
# Check the link if you are confused about an issue regarding the testing config.

# We manually designate which settings we will be using in an environment variable
# This is similar to what occurs in the `manage.py`
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webmark2.settings")


# `pytest` automatically calls this function once when tests are run.
def pytest_configure():
    settings.DEBUG = True
    # Test specific settings can be declared here, e.g.
    # settings.PASSWORD_HASHERS = (
    #     'django.contrib.auth.hashers.MD5PasswordHasher',
    # )
    django.setup()
