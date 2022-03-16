""" This module defined the top level url's

All URLs for the app are passed in to app.urls
All admin/ urls are handles by the django admin (not perf requirement)
"""

from django.contrib import admin
from django.urls import path,include
from django.urls import path


urlpatterns = [
    path('',include('app.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/',admin.site.urls),
]
