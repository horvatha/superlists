from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        texts = ('The first (ever) list item', 'Item the second')
        for item_text in texts:
            item = Item(text=item_text)
            item.save()

        items = Item.objects.all()
        self.assertEqual(items.count(), 2)

        for i in range(2):
            self.assertEqual(items[i].text, texts[i])


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

        home_page(request)

        items = Item.objects.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0].text, item_text)

    def test_home_page_redirects_after_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        item_text = 'A new list item'
        request.POST['item_text'] = item_text

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],
                         '/lists/the-only-list-in-the-world/')

    def test_home_page_saves_item_only_when_necessary(self):
        request = HttpRequest()

        home_page(request)

        items = Item.objects.all()
        self.assertEqual(items.count(), 0)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        item_texts = ('Item 1', 'Item 2')
        for i in item_texts:
            Item.objects.create(text=i)
            response = self.client.get('/lists/the-only-list-in-the-world/')
        for i in item_texts:
            self.assertContains(response, i)
