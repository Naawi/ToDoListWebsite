import time
from   selenium.webdriver.common.keys     import Keys
from   .base                              import FunctionalTest

class LayoutAndStylingTest( FunctionalTest ):

    def test_layout_and_styling( self ):
        #Go to home page
        self.browser.get( self.live_server_url )
        self.browser.set_window_size(1024, 768 )

        #check input box is centered
        inputbox = self.get_item_input_box()
        time.sleep( 1 )
        self.assertAlmostEqual( inputbox.location[ 'x' ] + inputbox.size[ 'width' ] / 2,
                                506,
                                delta = 5 )
                          
