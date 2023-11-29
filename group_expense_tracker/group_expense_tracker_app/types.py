import strawberry
from typing import List # noqa F401
from . import models


@strawberry.django.type(models.Posts)
class PostType:
    id: int # noqa A003
    title: str
    author: str
    message: str
