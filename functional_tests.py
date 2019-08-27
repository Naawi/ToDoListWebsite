import unittest
import time
from   selenium                       import webdriver
from   selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException

class NewVisitorTest( unittest.TestCase ):
    def setUp( self ):
        self.browser = webdriver.Firefox()

    def tearDown( self ):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later( self ):
        self.browser.get( 'http://localhost:8000' )
        self.assertIn( 'To-Do', self.browser.title )
        # test to-do header
        self.assertIn( 'To-Do', self.browser.title )
        header_text = self.browser.find_element_by_tag_name( 'h1' ).text
        self.assertIn('To-Do', header_text)
        # test to-do input box
        inputbox = self.browser.find_element_by_id( 'id_new_item' )
        self.assertEqual( inputbox.get_attribute( 'placeholder' ), 'Enter a to-do item' )
        # Type "Buy peacock feathers" in text box
        inputbox.click()
        inputbox.send_keys( 'Buy peacock feathers' )
        # Pressing enter should make page update
        inputbox.send_keys( Keys.ENTER )
        time.sleep( 1 )
        table = self.browser.find_element_by_id( 'id_list_table' )
        rows = self.browser.find_elements_by_tag_name( 'tr' )

        self.assertIn( '1: Buy peacock feathers', [ row.text for row in rows] )
        # Another box appears for new entry. Type "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id( 'id_new_item' )
        inputbox.click()
        inputbox.send_keys( 'Use peacock feathers to make a fly' )
        inputbox.send_keys( Keys.ENTER )
        time.sleep( 1 )
        # Page updates again
        table = self.browser.find_element_by_id( 'id_list_table' )
        rows = self.browser.find_elements_by_tag_name( 'tr' )
        self.assertIn( '2: Use peacock feathers to make a fly', [ row.text for row in rows] )

        # Unique url is generated, with an explanation

        # Visitng url should show same list

if __name__ == '__main__':
    unittest.main( warnings = 'ignore' )
