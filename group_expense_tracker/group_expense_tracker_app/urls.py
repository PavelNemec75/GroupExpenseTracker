
from django.urls import path
from . import views
from strawberry.django.views import GraphQLView

from .schema import schema


urlpatterns = [
    path("", views.index_view, name="index"),
    path("graphql", GraphQLView.as_view(schema=schema)),
]
