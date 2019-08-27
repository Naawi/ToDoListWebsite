import logging
from   django.urls            import resolve
from   django.test            import TestCase
from   lists.views            import home_page
from   django.http            import HttpRequest
from   django.template.loader import render_to_string


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
        request = HttpRequest()
        response = home_page( request )
        expected = render_to_string( 'home.html' )
        print('expected: ', expected)
        print('actual: ', response.content.decode())
        self.assertEqual( response.content.decode(), expected )

    def test_home_page_can_save_a_POST_request( self ):
        request = HttpRequest()
        request.method = 'POST'
        request.POST[ 'item_text' ] = 'A new list item'
        response = home_page( request )
        self.assertIn( 'A new list item', response.content.decode() )
        expected = render_to_string( 'home.html',
                                     { 'new_item_text': 'A new list item' } )
        self.assertEqual( response.content.decode(), expected )
