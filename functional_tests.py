from selenium import webdriver
import unittest

class NewVisitorTest( unittest.TestCase ):
    def setUp( self ):
        self.browser = webdriver.Firefox()

    def tearDown( self ):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later( self ):
        self.browser.get( 'http://localhost:8000' )
        self.assertIn( 'To-Do', self.browser.title )
        self.fail( 'Finish the test!' )
        # load to-do page

        # Type "Buy peacock feathers" in text box

        # Pressing enter should make page update

        # Another box appears for new entry

        # Type "Use peacock feathers to make a fly"

        # Page updates again

        # Unique url is generated, with an explanation

        # Visitng url should show same list

if __name__ == '__main__':
    unittest.main( warnings = 'ignore' )
