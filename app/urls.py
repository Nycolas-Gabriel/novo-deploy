from django.urls import path
from . import views
from .views import login_view, register_view, profile_view, change_password_view, item_list_view, cadastrar_item
from .views import CustomLogoutView 

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('items/', views.item_list_view, name='items'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
