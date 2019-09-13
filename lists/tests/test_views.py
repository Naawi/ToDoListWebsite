import re
import logging
from   django.urls            import resolve
from   django.test            import TestCase
from   lists.views            import home_page
from   django.http            import HttpRequest
from   django.template.loader import render_to_string
from   lists.models           import Item, List
from   django.utils.html      import escape
from   lists.forms            import ItemForm


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

    def test_homepage_uses_item_form( self ):
        response = self.client.get( '/' )
        self.assertIsInstance( response.context[ 'forms' ], ItemForm )


class ListViewTest( TestCase ):

    def test_displays_all_items( self ):
        lst = List.objects.create()
        Item.objects.create( text = 'itemey 1', list = lst )
        Item.objects.create( text = 'itemey 2', list = lst )

        response = self.client.get( '/lists/%d/' % ( lst.id ) )

        self.assertContains( response, 'itemey 1' )
        self.assertContains( response, 'itemey 2' )

    def test_uses_list_template( self ):
        lst = List.objects.create()
        response = self.client.get( '/lists/%d/' % ( lst.id ) )
        self.assertTemplateUsed( response, 'list.html' )

    def test_displays_only_items_for_that_list( self ):
        lst = List.objects.create()
        Item.objects.create( text = "itemey 1", list = lst )
        Item.objects.create( text = "itemey 2", list = lst )
        other_lst = List.objects.create()
        Item.objects.create( text = "other list item 1", list = other_lst )
        Item.objects.create( text = "other list item 2", list = other_lst )

        response = self.client.get( '/lists/%d/' % ( lst.id ) )

        self.assertContains( response, 'itemey 1' )
        self.assertContains( response, 'itemey 2' )
        self.assertNotContains( response, 'other list item 1' )
        self.assertNotContains( response, 'other list item 2' )

    def test_passes_correct_list_to_template( self ):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.get( '/lists/%d/' % ( correct_list.id ) )

        self.assertEqual( response.context[ 'list' ], correct_list )

    def test_validation_errors_end_up_on_lists_page( self ):
        lst = List.objects.create()
        response = self.client.post( f'/lists/{lst.id}/', data = { 'item_text': '' } )

        self.assertEqual( response.status_code, 200 )
        self.assertTemplateUsed( response, 'list.html' )
        expected_error = escape( "You can't have an empty list item" )
        self.assertContains( response, expected_error )
         

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
        new_list = List.objects.first()
        self.assertRedirects( response, '/lists/%d/' % ( new_list.id ) )

    def test_validation_errors_are_sent_back_to_homepage_template( self ):
        response = self.client.post( '/lists/new', data = { 'item_text': '' } )
        self.assertEqual( response.status_code, 200 )
        self.assertTemplateUsed( response, 'home.html' )
        expected_error = escape( "You can't have an empty list item" )
        self.assertContains( response, expected_error )

    def test_invalid_list_items_arent_saved( self ):
        self.client.post( '/lists/new', data={ 'item_text': '' })
        self.assertEqual( List.objects.count(), 0 )
        self.assertEqual( Item.objects.count(), 0 )

    def test_can_save_a_POST_request_to_an_existing_list( self ):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post( f'/lists/{correct_list.id}/', 
                          data = { 'item_text': 'A new item for an existing list' } )

        self.assertEqual( Item.objects.count(), 1 )
        new_item = Item.objects.first()
        self.assertEqual( new_item.text, 'A new item for an existing list' )
        self.assertEqual( new_item.list, correct_list )

    def test_POST_redirects_to_list_view( self ):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post( f'/lists/{correct_list.id}/',
                                     data = { 'item_text': 'A new item for an existing list' } )
        
        self.assertRedirects( response, f'/lists/{correct_list.id}/' ) 

