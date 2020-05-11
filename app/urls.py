from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index),
    path('TODO/', views.todo),
    path('client/', views.client2),
    path('admin/', include('app.url_admin')),
    path('client/change/<int:id>', views.client_change),
    path('client/delete/<int:id>', views.client_delete),
    path('client/create', views.client_create),
    path('provider/', views.provider),
    path('provider/create', views.provider_create),
    path('provider/delete/<int:id>', views.provider_delete),
    path('provider/change/<int:id>', views.provider_change),
    path('service/', views.service),
    path('service/create', views.service_create),
    path('service/delete/<int:id>', views.service_delete),
    path('service/change/<int:id>', views.service_change),
    path('rendered_service/create', views.rendered_service_create),
    path('rendered_service/', views.rendered_service),
    path('provided_service/', views.provided_service),
    path('provided_service/create', views.provided_service_create),
    path('casino/', views.casino)

]