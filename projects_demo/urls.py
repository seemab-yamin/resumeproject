from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.projects_demo, name="projects_demo_url"),
    path(
        "google-maps-scraper/",
        view=views.google_maps_scraper_demo,
        name="google_maps_scraper_demo_url",
    ),
    path(
        "download-results/<str:file_name>/",
        view=views.download_results,
        name="download_results_url",
    ),
]
