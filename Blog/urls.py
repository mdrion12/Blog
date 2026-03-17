from django.urls import path
from .views import (
    post_list,
    post_details,
    signup_view,
    post_create,
    post_update,
    post_delete,
    add_comment,
    like_post
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home / Post List
    path("", post_list, name='post_list'),

    # Post Details
    path("post/<int:id>/", post_details, name='post_details'),

    # Auth
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", signup_view, name="signup"),

    # Post CRUD
    path("post/create/", post_create, name='post_create'),
    path("post/update/<int:id>/", post_update, name='post_update'),
    path("post/delete/<int:id>/", post_delete, name='post_delete'),

    # Comment
    path("post/<int:id>/comment/", add_comment, name='add_comment'),

    # Like / Unlike
    path("post/<int:id>/like/", like_post, name='like_post'),
]