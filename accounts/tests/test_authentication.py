from django.test             import TestCase
from django.contrib.auth     import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models         import Token
from uuid import uuid4

User = get_user_model()


class AuthenticateTest( TestCase ):

    def test_returns_None_if_no_such_token( self ):
        result = PasswordlessAuthenticationBackend().authenticate( '00a000a0-a0aa-000a-0000-a00a000a0000' )
        self.assertIsNone( result )

    def test_returns_new_user_with_correct_email_if_token_exists( self ):
        email = 'a@b.com'
        token = Token.objects.create( email = email )
        user = PasswordlessAuthenticationBackend().authenticate( uid = token.uid )
        new_user = User.objects.get( email = email ) 
        self.assertEqual( user, new_user )

    def test_returns_existing_user_with_correct_email_if_token_exists( self ):
        email = 'a@b.com'
        existing_user = User.objects.create( email = email )
        token = Token.objects.create( email = email )
        user = PasswordlessAuthenticationBackend().authenticate( uid = token.uid )
        self.assertEqual( user, existing_user )


class GetUserTest( TestCase ):

    def test_gets_user_by_email( self ):
        User.objects.create( email = 'navin@example.com' )
        desired_user = User.objects.create( email = 'a@b.com' )
        found_user = PasswordlessAuthenticationBackend().get_user( 'a@b.com' )
        self.assertEqual( found_user, desired_user )

    def test_returns_None_if_no_user_with_that_email( self ):
        self.assertIsNone( PasswordlessAuthenticationBackend().get_user( 'a@b.com' ) )