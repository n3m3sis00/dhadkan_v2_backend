"""
WSGI config for dhadkan project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# project_path = "/home/deepak/Desktop/dhadkan"
# if project_path not in sys.path:
#     sys.path.append(project_path)
# app_path = "/home/deepak/Desktop/dhadkan/dhadkan"
# if app_path not in sys.path:
#     sys.path.append(app_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dhadkan.settings")

application = get_wsgi_application()
