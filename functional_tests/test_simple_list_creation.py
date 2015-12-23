#!/usr/bin/env python3
# coding: utf-8

"""functional_test for Test Driven Program Development by Harry Percival
"""

from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time


def sleep_a_bit():
    time.sleep(0)


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')
        sleep_a_bit()
        inputbox.send_keys('Repair the bicycle')
        inputbox.send_keys(Keys.ENTER)
        sleep_a_bit()
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Repair the bicycle')

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')
        sleep_a_bit()
        inputbox.send_keys('Take a bicycle tour')
        sleep_a_bit()
        inputbox.send_keys(Keys.ENTER)
        sleep_a_bit()
        for row_text in ('1: Repair the bicycle', '2: Take a bicycle tour'):
            self.check_for_row_in_list_table(row_text)

        # A new user Francis comes along the site
        self.browser.quit()
        # We use a new browser session to make sure there is no
        # trace of Edith's through cokies or etc
        self.browser = webdriver.Firefox()

        # Francis visits the home page
        # There is no sign of Edith's list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Repair the bicycle', page_text)
        self.assertNotIn('bicycle', page_text)

        # Francis starts a new list
        # There is no sign of Edith's list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        sleep_a_bit()
        self.assertNotEqual(francis_list_url, edith_list_url)
        self.check_for_row_in_list_table('1: Buy milk')

        # Again there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Repair the bicycle', page_text)
        self.assertIn('Buy milk', page_text)
