from django.urls import path

from .views import *


urlpatterns = [
    path(
        "applications/start/",
        StartApplicationView.as_view(),
        name="start-application",
    ),
    path(
        "applications/<uuid:pk>/",
        ApplicationDetailView.as_view(),
        name="application-detail",
    ),
    
    path(
        "educational-qualifications/",
        EducationalQualificationListView.as_view(), 
        name="educational-qualification-list",
    ),
    
    path(
    "applications/<uuid:pk>/documents/",
    ApplicationDocumentUploadView.as_view(),
    name="application-document-upload",
    ),
        
    path(
    "applications/<uuid:pk>/submit/",
    ApplicationSubmitView.as_view(),
    name="application-submit",
    ),
]