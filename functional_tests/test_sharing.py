from selenium import webdriver
from .base    import FunctionalTest
from .list_page import ListPage


def quit_if_possible( broswer ):
    try: broswer.quit()
    except: pass


class SharingTest( FunctionalTest ):
    
    def test_can_share_a_list_with_another_user( self ):
        # user1 is a logged in user
        self.create_pre_authenticated_session( 'user1@example.com' )
        user1_browser = self.browser
        self.addCleanup( lambda: quit_if_possible( user1_browser ) )

        # user2 is another user using the lists website
        user2_browser = webdriver.Firefox()
        self.addCleanup( lambda: quit_if_possible( user2_browser ) )
        self.browser = user2_browser
        self.create_pre_authenticated_session( 'user2@example.com')

        # user1 goes to the home page and starts a list
        self.browser = user1_browser
        self.browser.get( self.live_server_url )
        list_page = ListPage( self ).add_list_item( 'Become a successful contrepreneur' )

        # user1 sees a "Share this list" option
        share_box - list_page.get_share_box()
        self.assertEqual( share_box.get_attribute( 'placeholder' ), 'your-friend@example.com' )

        # they share their list
        # the page updates to say that it's shared with user2
        list_page.share_list_with( 'user2@example.com' )