from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from .models import Profile
from django.utils.translation import gettext_lazy as _
from random import random



class HelloView(View):
    welcome_message = _('welcome hello world!')
    def get(self, request: HttpRequest) -> HttpResponse:

        return HttpResponse(f'<h1>{self.welcome_message}<h1/>')
class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"

class UserProfileView(DetailView):
    template_name = 'myauth/user_profile.html'
    model = User
    context_object_name = 'user'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['pk']
        context['user'] = User.objects.get(pk=user_id)
        return context

class ChangeAvatarView(UpdateView, UserPassesTestMixin):
    model = Profile
    fields = 'avatar',
    template_name_suffix = '_update_form'

    def test_func(self):
        if self.request.user.is_staff:
            return True
        obj = self.get_object()
        return obj.user == self.request.use



    def get_success_url(self):
        return reverse(
            'myauth:user-profile',
            kwargs={'pk': self.object.user.pk},
        )





class UserListView(ListView):
    template_name = 'myauth/user_list.html'
    model = User
    context_object_name = 'users'



class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response



class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response

@cache_page(60*2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r} + {random()}")



@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")

class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})