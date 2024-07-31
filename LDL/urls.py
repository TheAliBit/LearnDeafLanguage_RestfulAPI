# from django.contrib import admin
# from django.urls import path, include
# import debug_toolbar
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('__debug__/', include(debug_toolbar.urls)),
#     path('api/', include('core.urls')),  # Assuming 'core.urls' contains your API endpoints
# ]

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

import core

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/registration/', include('core.urls')),
    path('api/apps/', include('words.urls')),
]
