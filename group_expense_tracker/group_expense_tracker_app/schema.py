import strawberry
from typing import List
from .models import Posts
from .types import PostType


# Query

@strawberry.type
class Query:
    @strawberry.field
    def xposts(self, title: str = None) -> List[PostType]:
        if title:
            post = Posts.objects.filter(title=title)
            return post
        return Posts.objects.all()


# Mutation

@strawberry.type
class Mutation:
    @strawberry.field
    def create_xpost(self, title: str, author: str, message: str) -> PostType:
        post = Posts(title=title, author=author, message=message)
        post.save()
        return post

    def update_xpost(self, id: int, title: str, author: str, message: str) -> PostType: # noqa A003
        post = Posts.objects.get(id=id)
        post.title = title
        post.author = author
        post.message = message
        post.save()
        return post

    # Defina a schema


schema = strawberry.Schema(query=Query, mutation=Mutation)
