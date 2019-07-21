from django.urls import resolve
from django.test import TestCase
from lists.views import home_page

# Create your tests here.
class HomePageTest( TestCase ):

    def test_root_url_resolves_to_home_page_views( self ):
        found = resolve( '/' )
        print(found)
        self.assertEqual( found.func, home_page )
