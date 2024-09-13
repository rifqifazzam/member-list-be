from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomToken

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        # Check if the Authorization header starts with 'Token '
        try:
            token_key = auth_header.split(' ')[1]
            token = CustomToken.objects.get(key=token_key)

            # Check if the token has expired
            if token.has_expired():
                token.delete()  # Delete expired token
                raise AuthenticationFailed('Token has expired')

            return (token.user, token)

        except CustomToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return None
