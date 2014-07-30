from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest
from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_the_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        item_text = 'A new list item'
        request.POST['item_text'] = item_text

        response = home_page(request)

        self.assertIn(item_text, response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': item_text}
        )
        self.assertEqual(response.content.decode(), expected_html)
