from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.post_list_view, name="list"),
    path("user/<str:username>/", views.user_list_view, name="user_list"),
    path("tags/<str:tag>/", views.tag_list_view, name="tag_list"),
    path("create/", views.create_view, name="create"),
    path("post/", views.post, name="post"),
]
