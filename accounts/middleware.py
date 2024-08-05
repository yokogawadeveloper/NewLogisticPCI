# middleware.py
from django.utils import timezone
from .models import ActiveUser


# Create your middleware.
class UpdateActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            now = timezone.now()
            ActiveUser.objects.update_or_create(
                user=request.user,
                defaults={'last_activity': now}
            )
        return response
