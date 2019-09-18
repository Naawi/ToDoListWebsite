from accounts.models import User, Token


class PasswordlessAuthenticationBackend( object ):

    def authenticate( self, request = None, uid = None, **kwargs ):
        try:
            token = Token.objects.get( uid = uid )
            user = User.objects.get( email = token.email )
            return user
        except User.DoesNotExist:
            return User.objects.create( email = token.email )
        except Token.DoesNotExist:
            return None

    def get_user( self, email ):
        try:
            return User.objects.get( email = email )
        except User.DoesNotExist:
            return None