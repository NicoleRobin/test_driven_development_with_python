#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        # self.browser = webdriver.Firefox()
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 伊丽丝听说有一个很酷的在线待办事项应用
        # 她去看了这个应用的首页
        self.browser.get(self.live_server_url)

        # 她注意到网页的标题和头部都包含'To-Do'这个词
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 应用邀请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 她在一个文本框中输入了'Buy peacock feathers'
        # 伊迪斯的爱好是使用假蝇做鱼饵钓鱼
        inputbox.send_keys('Buy peacock feathers')

        # 她按回车键后，被带到了一个新URL
        # 这个页面的待办事项清单中显示：'1：Buy peacock feathers'
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 她输入了'Use peacock feathers to make a fly'（使用孔雀羽毛做假蝇）
        # 伊迪斯做事很有条理
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # 伊迪斯想知道这个网站是否会记住它的清单

        # 页面再次更新，她的清单中显示了这两个待办事项
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 现在一个叫弗朗西斯的新用户访问了网站

        ## 我们使用一个新浏览器会话
        ## 确保依迪丝的信息不会从cookie中泄露出来
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # 弗朗西斯访问首页
        # 页面中看不到依迪丝的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # 弗朗西斯输入一个新待办事项，新建一个清单
        # 他不像依迪丝那样兴趣盎然
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # 弗朗西斯获得了他的唯一URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 这个页面还是没有依迪丝的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # 两个人都很满意，去睡觉了

    def test_layout_and_styling(self):
        # 依迪丝访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 她看到输入框完美地居中显示
        inputbox = self.browser.find_element_by_id('id_new_item')
        # print(inputbox.location)
        # print(inputbox.size)
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5,
        )

        # 她新建一个清单，看到输入框仍完美的居中显示
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5,
        )
