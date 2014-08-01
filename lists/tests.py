from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item, List


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        texts = ('The first (ever) list item', 'Item the second')
        for item_text in texts:
            item = Item(text=item_text, list=list_)
            item.save()

        saved_lists = List.objects.all()
        self.assertEqual(saved_lists.count(), 1)
        self.assertEqual(saved_lists[0], list_)
        items = Item.objects.all()
        self.assertEqual(items.count(), 2)

        for i in range(2):
            self.assertEqual(items[i].text, texts[i])
            self.assertEqual(items[i].list, list_)


class HomePageTest(TestCase):
    def test_root_url_resolves_the_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        item_text = 'A new list item'
        self.client.post(
            '/lists/new',
            {'item_text': item_text}
        )
        items = Item.objects.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0].text, item_text)

    def test_redirects_after_POST_request(self):
        item_text = 'A new list item'
        response = self.client.post(
            '/lists/new',
            {'item_text': item_text}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        list_ = List.objects.create()
        item_texts = ('Item 1', 'Item 2')
        for i in item_texts:
            Item.objects.create(text=i, list=list_)
            response = self.client.get('/lists/the-only-list-in-the-world/')
        for i in item_texts:
            self.assertContains(response, i)
