from django.urls import path
from .views import *
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path("", index, name="index"),
    path("lottery/", lottery, name="lottery"),
    path("search/", search, name="search"),
    path("about/", about, name="about"),
    path("masthead/", masthead, name="masthead"),
    path("comp/", comp, name="comp"),
    path("contact/", contact, name="contact"),
    path("features/", features, name="features"),
    path("starr/", starr, name="starr"),
    path("ads.txt", RedirectView.as_view(url=staticfiles_storage.url("ads.txt")))
]