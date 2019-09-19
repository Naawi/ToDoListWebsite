import time
import re
from   django.core                    import mail
from   selenium.webdriver.common.keys import Keys
from   .base                          import FunctionalTest

TEST_EMAIL = 'user@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest( FunctionalTest ):

    def test_can_get_email_link_to_log_in( self ):
        #user logs in
        self.browser.get( self.live_server_url )
        self.browser.find_element_by_name( 'email' ).send_keys( TEST_EMAIL )
        self.browser.find_element_by_name( 'email' ).send_keys( Keys.ENTER )

        # message appears telling user an email has been sent to them
        self.wait_for( lambda: self.assertIn( 'Check your email',
                                               self.browser.find_element_by_tag_name( 'body' ).text ) ) 
        

        # user check their email and find a message
        email = mail.outbox[ 0 ]
        self.assertIn( TEST_EMAIL, email.to )
        self.assertEqual( email.subject, SUBJECT )

        # email has a url ink in it
        self.assertIn( 'Use this link to log in', email.body )
        url_search = re.search( r'http://.+/.+$', email.body )
        if not url_search:
            self.fail( f'Could not find url in email body \n{email.body}' )
        url = url_search.group( 0 )
        self.assertIn( self.live_server_url, url )

        # user clicks link
        self.browser.get( url )

        # user is logged in!
        self.wait_to_be_logged_in( email = TEST_EMAIL )

        # user logs out
        #logout_link = self.wait_for( lambda: self.browser.find_element_by_link_text( 'Log out' ) )
        self.browser.find_element_by_link_text( 'Log out' ).click()
        self.wait_to_be_logged_out( email = TEST_EMAIL )