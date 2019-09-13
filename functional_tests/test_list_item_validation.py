from   selenium.webdriver.common.keys     import Keys
from   .base                              import FunctionalTest
from   unittest                           import skip

class ItemValidationTest( FunctionalTest ):

    def test_cannot_add_empty_list_items( self ):
        # user submits empty list item. Hits Enter on the empty input box

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank

        # user tries again with some text for the item, which now works

        # user submits a second blank list item

        # user receives a similar warning on the list page

        # user inputs some text in
        self.fail('write me!')                              
