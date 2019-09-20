import time
from   selenium                           import webdriver
from   selenium.webdriver.common.keys     import Keys
from   .base                              import FunctionalTest

class NewVisitorTest( FunctionalTest ):

    def test_can_start_a_list_for_one_user( self ):
        self.browser.get( self.live_server_url )
        self.assertIn( 'To-Do', self.browser.title )
        # test to-do header
        self.assertIn( 'To-Do', self.browser.title )
        header_text = self.browser.find_element_by_tag_name( 'h1' ).text
        self.assertIn('To-Do', header_text)
        # test to-do input box
        inputbox = self.get_item_input_box()
        self.assertEqual( inputbox.get_attribute( 'placeholder' ), 'Enter a to-do item' )
        # Type "Buy peacock feathers" in text box
        #inputbox.click()
        inputbox.send_keys( 'Buy peacock feathers' )
        # Pressing enter should make page update
        inputbox.send_keys( Keys.ENTER )
        time.sleep( 1 )
        self.wait_for_row_in_list_table( '1: Buy peacock feathers' )
        # Another box appears for new entry. Type "Use peacock feathers to make a fly"
        self.get_item_input_box().send_keys( 'Use peacock feathers to make a fly' )
        self.get_item_input_box().send_keys( Keys.ENTER )
        time.sleep( 1 )
        # Page updates again
        self.wait_for_row_in_list_table( '1: Buy peacock feathers' )
        self.wait_for_row_in_list_table( '2: Use peacock feathers to make a fly' )

    def test_multiple_users_can_start_lists_at_different_urls( self ):
        # user1 start a new todo list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys( 'Buy peacock feathers' )
        self.get_item_input_box().send_keys( Keys.ENTER )
        time.sleep( 1 )

        user1_list_url = self.browser.current_url
        self.assertRegex( user1_list_url, '/lists/.+' )
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # New user visits the home Page. Should be empty
        self.browser.get( self.live_server_url )
        page_text = self.browser.find_element_by_tag_name( 'body' ).text
        self.assertNotIn( 'Buy peacock feathers', page_text )
        self.assertNotIn( 'make a fly', page_text )

        # New user starts a new list by entering a new item
        self.get_item_input_box().send_keys( 'Buy milk' )
        self.get_item_input_box().send_keys( Keys.ENTER )
        time.sleep( 1 )

        # New user gets their own url
        user2_list_url = self.browser.current_url
        self.assertRegex( user2_list_url, '/lists/.+' )
        self.assertNotEqual( user2_list_url, user1_list_url )

        # Check there's no trace of user1
        page_text = self.browser.find_element_by_tag_name( 'body' ).text
        self.assertNotIn( 'Buy peacock feathers', page_text )
        self.assertIn( 'Buy milk', page_text)
