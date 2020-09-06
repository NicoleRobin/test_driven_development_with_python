from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists import views

# Create your tests here.


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, views.home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.home_page(request)
        expected_html = render_to_string('home.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        # 真正的逻辑返回的结果
        response = views.home_page(request)
        self.assertIn('A new list item', response.content.decode())
        # 直接调用render_to_string返回的结果
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )
        self.assertEqual(response.content.decode(), expected_html)
