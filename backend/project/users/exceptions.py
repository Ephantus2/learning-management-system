from django_ratelimit.exceptions import Ratelimited
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    if isinstance(exc, Ratelimited):
        return Response(
            {
                "detail": "Rate limit exceeded. Try again in a minute."
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )

    return exception_handler(exc, context)