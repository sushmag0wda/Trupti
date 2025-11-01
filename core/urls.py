from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.splash, name="splash"),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("donations/", views.donation_list, name="donation_list"),
    path("donations/create/", views.donation_create, name="donation_create"),
    path("donations/<int:pk>/edit/", views.donation_edit, name="donation_edit"),
    path("donations/<int:pk>/delete/", views.donation_delete, name="donation_delete"),
    path("donations/<int:pk>/request/", views.create_food_request, name="create_food_request"),
    path("requests/", views.request_list, name="request_list"),
    path("requests/<int:pk>/update/", views.update_request_status, name="update_request_status"),
]
