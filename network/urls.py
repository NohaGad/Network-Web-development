
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.post_view, name="posts"),
    path("follow", views.follow_view, name="follow"),
    path("post/<int:post_id>", views.post_edit, name="post"),
    path("like/<int:post_id>", views.like_view, name="like"),
    path("unlike/<int:post_id>", views.unlike_view, name="unlike")
]
