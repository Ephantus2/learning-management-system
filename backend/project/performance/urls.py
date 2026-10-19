from django.urls import path
from .views import TranscriptDownloadView

urlpatterns = [
    path(
        "transcript/download/",
        TranscriptDownloadView.as_view()
    )
]