from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.career_anchor, name="careeranchor"),
    path("stats", view=views.stats, name="stats")
]