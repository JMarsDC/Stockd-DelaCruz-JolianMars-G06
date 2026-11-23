from django.urls import path

from . import views

urlpatterns = [
    path("", views.storage_list, name="storage_list"),
    path("new/", views.storage_create, name="storage_create"),
    path("<int:pk>/", views.storage_detail, name="storage_detail"),
    path("<int:pk>/edit/", views.storage_edit, name="storage_edit"),
    path("<int:pk>/delete/", views.storage_delete, name="storage_delete"),
]