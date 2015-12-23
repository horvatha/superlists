#!/usr/bin/env python3
# coding: utf-8

"""functional_test for Test Driven Program Development by Harry Percival
"""

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.server_url)
        width, height = 1024, 768
        self.browser.set_window_size(width, height)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_tag_name('input')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            width/2,
            delta=3
        )

        # She starts a new list and see the input box is nicely centered there
        # too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_tag_name('input')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            width/2,
            delta=3
        )
