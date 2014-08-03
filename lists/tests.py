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
        new_list = List.objects.all()[0]
        self.assertRedirects(response, '/lists/{}/'.format(new_list.id))


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        List.objects.create()  # other list
        correct_list = List.objects.create()

        item_text = 'A new item for an existing list'
        self.client.post(
            '/lists/{}/new_item'.format(correct_list.id),
            {'item_text': item_text}
        )
        items = Item.objects.all()
        self.assertEqual(items.count(), 1)
        new_item = items[0]
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        List.objects.create()  # other list
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{}/new_item'.format(correct_list.id),
            {'item_text':  'A new item for an existing list'}
        )
        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_item_texts = ('Item 1', 'Item 2')
        other_item_texts = ('Other Item 1', 'Other Item 2')

        correct_list = List.objects.create()
        for i in correct_item_texts:
            Item.objects.create(text=i, list=correct_list)
        other_list = List.objects.create()
        for i in other_item_texts:
            Item.objects.create(text=i, list=other_list)

        response = self.client.get('/lists/{}/'.format(correct_list.id))

        for i in correct_item_texts:
            self.assertContains(response, i)
        for i in other_item_texts:
            self.assertNotContains(response, i)

    def test_displays_all_list_items(self):
        list_ = List.objects.create()
        item_texts = ('Item 1', 'Item 2')
        for i in item_texts:
            Item.objects.create(text=i, list=list_)
            response = self.client.get('/lists/{}/'.format(list_.id))
        for i in item_texts:
            self.assertContains(response, i)

    def test_passes_correct_list_to_template(self):
        List.objects.create()  # other list
        correct_list = List.objects.create()
        response = self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)
