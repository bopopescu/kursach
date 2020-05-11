from django.urls import path
from . import views
urlpatterns = [
    path('', views.admin),
    path('permission_check/', views.pemission_check),
    path('registrations/', views.register_new_user),
    path('add_pex', views.add_permission_to_user),
    path('check_perm', views.check_perms),
    path('user/delete/<int:id>', views.delete),
    path('user', views.user),
    path('user/change/<int:id>', views.change_user)

]