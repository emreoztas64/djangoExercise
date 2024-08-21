from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.post_list_view, name="list"),
    path("create/", views.create_view, name="create"),
    path("post/", views.post, name="post"),
]
