from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostListView.as_view(), name="list"),
    path("user/<str:username>/", views.PostListView.as_view(), name="user_list"),
    path("tag/<str:tag>/", views.PostListView.as_view(), name="tag_list"),
    path("create/", views.PostCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.PostUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="delete"),
]
