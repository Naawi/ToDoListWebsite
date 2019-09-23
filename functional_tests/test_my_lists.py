from .base import FunctionalTest
from .server_tools import create_session_on_server
import time


class MyListsTest( FunctionalTest ):

    def test_logged_in_users_lists_are_saved_as_my_lists( self ):
        # user1 is a logged-in user
        self.create_pre_authenticated_session( 'user@example.com' )

        # user1 goes to the homepage and starts a list
        self.browser.get( self.live_server_url )
        self.add_list_item( 'Reticulate splines' )
        self.add_list_item( 'Immanentize eschaton' )
        first_list_url = self.browser.current_url

        # user1 sees a "My lists" link and clicks on it
        self.browser.find_element_by_link_text( 'My lists' ).click()

        # user1 sees their list is there, named after the first list item
        self.wait_for( lambda: self.browser.find_element_by_link_text( 'Reticulate splines' ) )
        self.browser.find_element_by_link_text( 'Reticulate splines' ).click()
        self.wait_for( lambda: self.assertEqual( self.browser.current_url, first_list_url ) )

        # user1 starts another list
        self.browser.get( self.live_server_url )
        self.add_list_item( 'Take iron tablets' )
        second_list_url = self.browser.current_url

        # the new list appears under "my lists" page
        self.browser.find_element_by_link_text( 'My lists' ).click()
        self.wait_for( lambda: self.browser.find_element_by_link_text( 'Take iron tablets' ) )
        self.browser.find_element_by_link_text( 'Take iron tablets' ).click()
        self.wait_for( lambda: self.assertEqual( self.browser.current_url, second_list_url ) )

        # user1 logs out
        self.browser.find_element_by_link_text( 'Log out' ).click()
        self.wait_for( lambda: self.assertEqual( self.browser.find_elements_by_link_text( 'My lists' ), [] ) )
        
