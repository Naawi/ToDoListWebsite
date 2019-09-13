from   selenium.webdriver.common.keys     import Keys
from   .base                              import FunctionalTest
from   unittest                           import skip

class ItemValidationTest( FunctionalTest ):

    def test_cannot_add_empty_list_items( self ):
        # user submits empty list item. Hits Enter on the empty input box
        self.browser.get( self.live_server_url )
        self.browser.find_element_by_id( 'id_new_item' ).send_keys( Keys.ENTER )

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for( self.assertEqual(
            self.browser.find_element_by_css_selector( '.has-error' ).text,
            "You can't have an empty list item"
        ) )

        # user tries again with some text for the item, which now works
        self.browser.find_element_by_id( 'id_new_item' ).send_keys( 'Buy strawberries' )
        self.browser.find_element_by_id(' id_new_item' ).send_keys( Keys.ENTER )
        self.wait_for_row_in_list_table( '1: Buy strawberries' )                           

        # user submits a second blank list item
        self.browser.find_element_by_id( 'id_new_item' ).send_keys( Keys.Enter )

        # user receives a similar warning on the list page
        self.wait_for( self.assertEqual(
            self.browser.find_element_by_css_selector( '.has-error' ).text,
            "You can't have an empty list item"
        ) )

        # user inputs some text in
        self.browser.find_element_by_id( 'id_new_item' ).send_keys( 'Make strawberry jam' )
        self.browser.find_element_by_id( 'id_new_item' ).send_keys( Keys.ENTER )
        self.wait_for_row_in_list_table( '1: Buy strawberries' )  
        self.wait_for_row_in_list_table( '2: Make strawberry jam' )  
