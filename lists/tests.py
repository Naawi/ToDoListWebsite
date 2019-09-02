import re
import logging
from   django.urls            import resolve
from   django.test            import TestCase
from   lists.views            import home_page
from   django.http            import HttpRequest
from   django.template.loader import render_to_string
from   lists.models           import Item, List


# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your tests here.
class HomePageTest( TestCase ):

    @staticmethod
    def remove_csrf( html_code ):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def assertEqualExceptCSRF( self, html_code1, html_code2 ):
        return self.assertEqual(
            self.remove_csrf(html_code1),
            self.remove_csrf(html_code2)
        )

    def test_root_url_resolves_to_home_page_views( self ):
        found = resolve( '/' )
        self.assertEqual( found.func, home_page )

    def test_home_page_returns_correct_html( self ):
        request = HttpRequest()
        response = home_page( request )
        expected = render_to_string( 'home.html', request = request )
        self.assertEqualExceptCSRF( response.content.decode(), expected )


class ListAndItemModelsTest( TestCase ):

    def test_saving_and_retrieving_items( self ):
        lst = List()
        lst.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = lst
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = lst
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual( saved_list, lst )

        saved_items = Item.objects.all()
        self.assertEqual( saved_items.count(), 2 )

        first_saved_item = saved_items[ 0 ]
        second_saved_item = saved_items[ 1 ]
        self.assertEqual( first_item.text, 'The first (ever) list item' )
        self.assertEqual( first_item.list, lst )
        self.assertEqual( second_item.text, 'Item the second' )
        self.assertEqual( second_item.list, lst )



class ListViewTest( TestCase ):

    def test_displays_all_items( self ):
        lst = List.objects.create()
        Item.objects.create( text = 'itemey 1', list = lst )
        Item.objects.create( text = 'itemey 2', list = lst )

        response = self.client.get( '/lists/global-list/' )

        self.assertContains( response, 'itemey 1' )
        self.assertContains( response, 'itemey 2' )

    def test_uses_list_template( self ):
        response = self.client.get( '/lists/global-list/' )
        self.assertTemplateUsed( response, 'list.html' )


class NewListTest( TestCase ):

    def test_saving_a_POST_request( self ):
        self.client.post( '/lists/new', data = { 'item_text': 'A new list item' } )
        # request = HttpRequest()
        # request.method = 'POST'
        # request.POST[ 'item_text' ] = 'A new list item'
        # response = home_page( request )

        self.assertEqual( Item.objects.count(), 1 )
        new_item = Item.objects.first()
        self.assertEqual( new_item.text, 'A new list item' )

    def test_redirects_after_POST( self ):
        response = self.client.post( '/lists/new', data = { 'item_text': 'A new list item' } )

        self.assertRedirects( response, '/lists/global-list/' )