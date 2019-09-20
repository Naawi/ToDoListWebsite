from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


class MyListsTest( FunctionalTest ):

    def create_pre_authenticated_session( self, email ):
        if self.staging_server:
            session_key = create_session_on_server( self.staging_server, email )
        else:
            session_key = create_pre_authenticated_session( email )

        ## To set a cookie we first need to visit the domain
        self.browser.get( self.live_server_url + "/404_no_such_url" )
        self.browser.add_cookie( dict( name = settings.SESSION_COOKIE_NAME,
                                       value = session_key,
                                       path = '/' ) )

    def test_logged_in_users_lists_Are_saved_as_my_lists( self ):
        email = 'a@b.com'
        self.browser.get( self.live_server_url )
        self.wait_to_be_logged_out( email )

        # store session key for user. user should be logged in
        self.create_pre_authenticated_session( email )
        self.browser.get( self.live_server_url )
        self.wait_to_be_logged_in( email )