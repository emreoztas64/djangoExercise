from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.post_list_view, name="list"),
    path("user/<str:username>/", views.post_list_view, name="user_list"),
    path("tag/<str:tag>/", views.post_list_view, name="tag_list"),
    path("create/", views.create_view, name="create"),
    path("update/<int:id>/", views.update_view, name="update"),
    path("delete/<int:id>/", views.delete, name="delete"),
]
