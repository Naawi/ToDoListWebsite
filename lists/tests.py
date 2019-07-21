from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your tests here.
class HomePageTest( TestCase ):

    def test_root_url_resolves_to_home_page_views( self ):
        found = resolve( '/' )
        self.assertEqual( found.func, home_page )

    def test_home_page_returns_correct_html( self ):
        request = HttpRequest()
        response = home_page( request )
        # logger.warning( "response content", response.content )
        # result = response.content.decode( 'utf-8' )
        self.assertTrue( response.content.startswith( b'<html>' ) )
        self.assertIn( b'<title>To-Do lists</title>', response.content )
        self.assertTrue( response.content.endswith( b'</html>' ) )
