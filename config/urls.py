from django.urls import include, path

from api.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("api/", include("api.urls")),
]
