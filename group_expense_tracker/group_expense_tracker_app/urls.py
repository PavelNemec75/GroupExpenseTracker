
from django.urls import include, path
from . import views
from strawberry.django.views import GraphQLView

from .schema import schema
from .views import login_view, logout_view

urlpatterns = [
    path("", views.index_view, name="index"),
    path("graphql", GraphQLView.as_view(schema=schema)),
    path("auth/", include("social_django.urls", namespace="social")),
    path('auth/complete/google-oauth2/', views.google_auth_complete, name='google-auth-complete'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
