from django.urls.conf import path
from .views import dashboard

urlpatterns = [path("", dashboard, name="dashboard")]
