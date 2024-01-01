from django.http import JsonResponse


class StrawberryLoginMiddleware:
    def __init__(self, get_response):
        print("StrawberryLoginMiddleware created")
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/graphql") and request.user.is_anonymous:
            return JsonResponse({"error": "Not logged in"}, status=403)
        return self.get_response(request)
