from django.contrib import admin
from django.urls import path, include

import leads

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include('leads.urls', namespace='leads'))
]
