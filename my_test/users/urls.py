from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.registration_view, name='registration_view'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('login/', views.login_view, name='login_view'),
]
