import unittest
import time
from   selenium                           import webdriver
from   selenium.webdriver.common.keys     import Keys
from   django.contrib.staticfiles.testing import StaticLiveServerTestCase


class NewVisitorTest( StaticLiveServerTestCase ):
    def setUp( self ):
        self.browser = webdriver.Firefox()

    def tearDown( self ):
        self.browser.quit()

    def check_for_row_in_list_table( self, row_text ):
        table = self.browser.find_element_by_id( 'id_list_table' )
        rows = table.find_elements_by_tag_name( 'tr' )
        self.assertIn( row_text, [ row.text for row in rows ] )

    def test_can_start_a_list_and_retrieve_it_later( self ):
        self.browser.get( self.live_server_url )
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
        user1_list_url = self.browser.current_url
        self.assertRegex( user1_list_url, '/lists/.+' )
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

        ## New user uses the site. Use browser session to make sure that
        ## no information of previous user is coming through cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # New user visits the home Page. Should be empty
        self.browser.get( self.live_server_url )
        page_text = self.browser.find_element_by_tag_name( 'body' ).text
        self.assertNotIn( 'Buy peacock feathers', page_text )
        self.assertNotIn( 'make a fly', page_text )

        # New user starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id( 'id_new_item' )
        inputbox.click()
        inputbox.send_keys( 'Buy milk' )
        inputbox.send_keys( Keys.ENTER )
        time.sleep( 1 )

        # New user gets their own url
        user2_list_url = self.browser.current_url
        self.assertRegex( user2_list_url, '/lists/.+' )
        self.assertNotEqual( user2_list_url, user1_list_url )

        # Check there's no trace of user1
        page_text = self.browser.find_element_by_tag_name( 'body' ).text
        self.assertNotIn( 'Buy peacock feathers', page_text )
        self.assertIn( 'Buy milk', page_text)

    def test_layout_and_styling( self ):
        #Go to home page
        self.browser.get( self.live_server_url )
        self.browser.set_window_size(1024, 768 )

        #check input box is centered
        inputbox = self.browser.find_element_by_id( 'id_new_item' )
        time.sleep(2)
        self.assertAlmostEqual( inputbox.location[ 'x' ] + inputbox.size[ 'width' ] / 2,
                                512,
                                delta = 5 )
