from django.urls import path

from django.contrib.auth.views import LogoutView

from .views import *


urlpatterns = [
    # Login
    path(
        "login/",
        CustomLoginView.as_view(),
        name="login",
    ),
    
    # Logout
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),


    # Dashboard
    path(
        "dashboard/",
        DashboardView.as_view(),
        name="dashboard",
    ),

    # Applications
    path(
        "applications/",
        ApplicationsView.as_view(),
        name="applications",
    ),

    # Students
    path(
        "students/",
        StudentListView.as_view(),
        name="students",
    ),

    # Documents
    path(
        "documents/",
        DocumentsView.as_view(),
        name="documents",
    ),

    # Administrators
    path(
        "users/",
        UsersView.as_view(),
        name="users",
    ),

    # Settings
    path(
        "settings/",
        SettingsView.as_view(),
        name="settings",
    ),
    
    # path("logout/", LogoutView.as_view(), name="logout"),

]