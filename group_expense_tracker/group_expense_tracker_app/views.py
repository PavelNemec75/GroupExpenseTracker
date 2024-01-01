from django.shortcuts import render
from social_django.views import complete as social_complete
from django.contrib.auth import logout
from django.shortcuts import redirect


def index_view(request):
    context = {"title": "API"}
    return render(request, "index.html", context)


def google_auth_complete(request, *args, **kwargs):
    return social_complete(request, 'google-oauth2', *args, **kwargs)


def login_view(request):
    return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('/')
