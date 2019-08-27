from unittest import TestCase
import time
from   selenium                       import webdriver
from   selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from lists.models import Item

class NewVisitorTest( TestCase ):
    def setUp( self ):
        self.browser = webdriver.Firefox()

    def tearDown( self ):
        self.browser.quit()

    def check_for_row_in_list_table( self, row_text ):
        table = self.browser.find_element_by_id( 'id_list_table' )
        rows = table.find_elements_by_tag_name( 'tr' )
        self.assertIn( row_text, [ row.text for row in rows ] )

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
        self.check_for_row_in_list_table( '1: Buy peacock feathers' )
        # Another box appears for new entry. Type "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id( 'id_new_item' )
        inputbox.click()
        inputbox.send_keys( 'Use peacock feathers to make a fly' )
        inputbox.send_keys( Keys.ENTER )
        time.sleep( 1 )
        # Page updates again
        self.check_for_row_in_list_table( '1: Buy peacock feathers' )
        self.check_for_row_in_list_table( '2: Use peacock feathers to make a fly' )
        self.assertIn( '2: Use peacock feathers to make a fly', [ row.text for row in rows] )

        # Unique url is generated, with an explanation

        # Visitng url should show same list

class ItemModelTest( TestCase ):

    def test_saving_and_retrieving_items( self ):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.ojects.all()
        self.assertEqual( saved_items.count(), 2 )

        first_saved_item = saved_items[ 0 ]
        second_saved_item = saved_items[ 1 ]
        self.assertEqual( first_item.text, 'The first (ever) list item' )
        self.assertEqual( second_item.text, 'Item the second' )

if __name__ == '__main__':
    unittest.main( warnings = 'ignore' )
