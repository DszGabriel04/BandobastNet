"""
WSGI config for bandobast project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
# import sys
from django.core.wsgi import get_wsgi_application

# # Add the project directory to the PYTHONPATH
# sys.path.append('/home/your-username/your-project-directory')

# # Set the default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bandobast.settings')

# # Create the WSGI application
application = get_wsgi_application()
app = application
