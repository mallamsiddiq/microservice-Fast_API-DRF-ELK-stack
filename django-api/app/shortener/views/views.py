from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from shortener.models import ShortenedURL
from shortener.serializers.serializers import ShortenedURLSerializer, PublicShortenedURLSerializer
from shortener.tasks import log_click_to_fastapi


class ShortenedURLViewSet(viewsets.ModelViewSet):
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return URLs belonging to the logged-in user
        return self.queryset.filter(owner=self.request.user)
    
class PublicShortenedURLViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShortenedURL.objects.all()
    serializer_class = PublicShortenedURLSerializer
    permission_classes = [AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        long_code = self.get_object()  # Get the ShortenedURL object
        res = super().retrieve(request, *args, **kwargs)  # Call the parent retrieve method

        # Extract IP address and user agent from the request
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')

        # Call the Celery task to log the click
        log_click_to_fastapi.delay(
            short_code=long_code.short_code,
            user_agent=user_agent,
            ip_address=ip_address,
        )

        return res