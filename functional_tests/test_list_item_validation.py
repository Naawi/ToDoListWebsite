from   selenium.webdriver.common.keys     import Keys
from   .base                              import FunctionalTest
from   unittest                           import skip
import time

class ItemValidationTest( FunctionalTest ):

    def test_cannot_add_empty_list_items( self ):
        # user submits empty list item. Hits Enter on the empty input box
        self.browser.get( self.live_server_url )
        inputbox = self.get_item_input_box()
        #inputbox.click()
        inputbox.send_keys( Keys.ENTER )
        time.sleep( 0.5 )

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for( lambda: self.assertEqual(
            self.browser.find_element_by_css_selector( '.has-error' ).text,
            "You can't have an empty list item"
        ) )

        # user tries again with some text for the item, which now works
        inputbox = self.get_item_input_box()
        #inputbox.click()
        inputbox.send_keys( 'Buy strawberries' )
        inputbox.send_keys( Keys.ENTER )
        time.sleep( 0.5 )
        self.wait_for_row_in_list_table( '1: Buy strawberries' )                           

        # user submits a second blank list item
        inputbox = self.get_item_input_box()
        #inputbox.click()
        inputbox.send_keys( Keys.ENTER )
        time.sleep( 0.5 )
        # user receives a similar warning on the list page
        self.wait_for( lambda: self.assertEqual(
            self.browser.find_element_by_css_selector( '.has-error' ).text,
            "You can't have an empty list item"
        ) )

        # user inputs some text in
        inputbox = self.get_item_input_box()
        #inputbox.click()
        inputbox.send_keys( 'Make strawberry jam' )
        inputbox.send_keys( Keys.ENTER )
        time.sleep( 0.5 )
        self.wait_for_row_in_list_table( '1: Buy strawberries' )  
        self.wait_for_row_in_list_table( '2: Make strawberry jam' )  
