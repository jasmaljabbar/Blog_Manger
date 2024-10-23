from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser

class JWTCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: self._get_user(request))
        return self.get_response(request)

    def _get_user(self, request):
        access_token = request.COOKIES.get('access_token')
        
        if not access_token:
            return AnonymousUser()

        try:
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(access_token)
            user = jwt_auth.get_user(validated_token)
            return user
        except:
            return AnonymousUser()
