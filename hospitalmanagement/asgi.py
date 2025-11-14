

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospitalmanagement.settings')
#defult to say hospitakmanagement.setting use

application = get_asgi_application()
#It creates a connection between your Django project and the ASGI server