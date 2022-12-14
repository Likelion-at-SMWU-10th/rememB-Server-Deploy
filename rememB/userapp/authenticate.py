from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, CSRFCheck

from django.conf import settings
from .models import User
import jwt


class SafeJWTAuthentication(BaseAuthentication):
    """
    JWT Authentication
    헤더의 jwt 값을 디코딩해 얻은 user_id 값을 통해서 유저 인증 여부를 판단한다.
    """
    
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        
        if not authorization_header:
            return None
            
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed('access_token is wrong')
        
        user = User.objects.filter(id=payload['user_id']).first()
        
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')
        
        # self.enforce_csrf(request)
        return (user,None)

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation
        """
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')