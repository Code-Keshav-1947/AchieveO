from django.urls import path
from . import views

urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("create/", views.order_create, name="order_create"),
    path("<int:pk>/edit/", views.order_edit, name="order_edit"),
    path("<int:pk>/delete/", views.order_delete, name="order_delete"),
    path("<int:pk>/update-status/", views.order_update_status, name="order_update_status"),
    path("<int:pk>/invoice/", views.order_invoice, name="order_invoice"),
    path("export-csv/", views.order_export_csv, name="order_export_csv"),
]
