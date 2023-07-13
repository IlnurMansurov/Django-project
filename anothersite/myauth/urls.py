from django.contrib.auth.views import LoginView
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    AboutMeView,
    RegisterView,
    FooBarView,
    UserProfileView,
    UserListView,
    ChangeAvatarView,
    HelloView,



)

app_name = "myauth"

urlpatterns = [
    # path("login/", login_view, name="login"),
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),

    path("hello/", HelloView.as_view(), name="hello"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),

    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),

    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),
    path('foo-bar/', FooBarView.as_view(), name='foo-bar'),
    path('user_list/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('change_avatar/<int:pk>/', ChangeAvatarView.as_view(), name='change_avatar')
]
