import unittest
import logging
from   django.test            import TestCase
from   lists.models           import Item, List
from   django.utils.html      import escape
from   lists.forms            import ( DUPLICATE_ITEM_ERROR,
                                       EMPTY_ITEM_ERROR,
                                       ExistingListItemForm, ItemForm, NewListForm )
from   django.contrib.auth    import get_user_model
from   unittest               import skip
from   unittest.mock          import patch, Mock
from   lists.views            import new_list
from   django.http            import HttpRequest

# Get an instance of a logger
logger = logging.getLogger(__name__)
User = get_user_model()


# Create your tests here.
class HomePageTest( TestCase ):

    def test_uses_home_template( self ):
        response = self.client.get( '/' )
        self.assertTemplateUsed( response, 'home.html' )

    def test_homepage_uses_item_form( self ):
        response = self.client.get( '/' )
        self.assertIsInstance( response.context[ 'form' ], ItemForm )


class ListViewTest( TestCase ):

    def post_invalid_input( self ):
        lst = List.objects.create()
        return self.client.post( f'/lists/{lst.id}/', data = { 'text': '' } )

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


    def test_for_invalid_input_nothing_saved_to_db( self ):
        self.post_invalid_input()
        self.assertEqual( Item.objects.count(), 0 )

    def test_for_invalid_input_renders_list_template( self ):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed( response, 'list.html' )

    def test_for_invalid_input_passes_form_to_template( self ):
        response = self.post_invalid_input()
        self.assertIsInstance( response.context['form'], ItemForm )

    def test_for_invalid_input_shows_error_on_page( self ):
        response = self.post_invalid_input()
        self.assertContains( response, escape( EMPTY_ITEM_ERROR ) )

    def test_duplicate_item_validation_errors_end_up_on_lists_page( self ):
        lst1 = List.objects.create()
        item1 = Item.objects.create( list = lst1, text = 'textey' )
        response = self.client.post( f'/lists/{lst1.id}/', data = { 'text': 'textey' } )

        expected_error = escape( DUPLICATE_ITEM_ERROR )
        self.assertContains( response, expected_error )
        self.assertTemplateUsed( response, 'list.html' )
        self.assertEqual( Item.objects.all().count(), 1 )

    def test_display_item_form( self ):
        lst = List.objects.create()
        response = self.client.get( f'/lists/{lst.id}/' )
        self.assertIsInstance( response.context[ 'form' ], ExistingListItemForm )
        self.assertContains( response, 'name="text"' )
         
    def test_for_invalid_input_passes_form_to_template( self ):
        response = self.post_invalid_input()
        self.assertIsInstance( response.context[ 'form' ], ExistingListItemForm )

    
@patch( 'lists.views.NewListForm' )
class NewListViewUnitTest( unittest.TestCase ):

    def setUp( self):
        self.request = HttpRequest()
        self.request.POST[ 'text' ] = 'new list item'
        self.request.user = Mock()

    @patch( 'lists.views.redirect' )
    def test_passes_POST_data_to_NewListForm( self, mock_redirect, mockNewListForm ):
        new_list( self.request )
        mockNewListForm.assert_called_once_with( data = self.request.POST )

    @patch( 'lists.views.redirect' )
    def test_saves_form_with_owner_if_form_valid( self, mock_redirect, mockNewListForm ):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True

        response = new_list( self.request )
        self.assertEqual( response, mock_redirect.return_value )
        mock_form.save.assert_called_once_with( owner = self.request.user )

    @patch( 'lists.views.render' )
    def test_renders_home_template_with_form_if_form_invalid( self, mock_render, mockNewListForm ):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        response = new_list( self.request )

        self.assertEqual( response, mock_render.return_value )
        mock_render.assert_called_once_with( self.request, 'home.html', { 'form': mock_form } )

    def test_does_not_save_if_form_invalid( self, mockNewListForm ):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list( self.request )
        self.assertFalse( mock_form.save.called )

    @patch( 'lists.views.redirect' )
    def test_redirects_to_form_returned_object_if_form_valid( 
        self, mock_redirect, mockNewListForm
    ):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True

        response = new_list( self.request )

        self.assertEqual( response, mock_redirect.return_value )
        mock_redirect.assert_called_once_with( mock_form.save.return_value )


class NewListViewIntegratedTest( TestCase ):

    def test_saving_a_POST_request( self ):
        self.client.post( '/lists/new', data = { 'text': 'A new list item' } )
        # request = HttpRequest()
        # request.method = 'POST'
        # request.POST[ 'text' ] = 'A new list item'
        # response = home_page( request )

        self.assertEqual( Item.objects.count(), 1 )
        new_item = Item.objects.first()
        self.assertEqual( new_item.text, 'A new list item' )

    def test_for_invalid_input_doesnt_save_but_shows_errors( self ):
        response = self.client.post( '/lists/new', data={ 'text': '' } )
        self.assertEqual( List.objects.count(), 0 )
        self.assertContains( response, escape( EMPTY_ITEM_ERROR ) )

    def test_list_owner_is_saved_if_user_is_authenticated( self ):
        user = User.objects.create( email = 'navin@b.com' )
        self.client.force_login( user )
        self.client.post( '/lists/new', data = { 'text': 'new item' } )
        lst = List.objects.first()
        self.assertEqual( lst.owner, user )



class MyListsTest( TestCase ):

    def test_my_lists_url_renders_my_lists_template( self ):
        correct_user = User.objects.create( email = 'n@b.com' )
        response = self.client.get( '/lists/users/n@b.com' )
        self.assertTemplateUsed( response, 'my_lists.html' )

    def test_passes_correct_owner_to_template(self):
        User.objects.create( email = 'wrong@owner.com' )
        correct_user = User.objects.create( email = 'navin@b.com' )
        response = self.client.get( '/lists/users/navin@b.com' )
        self.assertEqual( response.context[ 'owner' ], correct_user )

    

