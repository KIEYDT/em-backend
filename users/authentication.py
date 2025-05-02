from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

class CookieJWTAuthenticatation(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return None
        try:
            token = AccessToken(access_token)
            user_id = token.get("user_id")  # or token['user_id']
            User = get_user_model()
            user = User.objects.get(id=user_id)
            return (user, None)  # ✅ Correct: return user
        except Exception:
            return None
