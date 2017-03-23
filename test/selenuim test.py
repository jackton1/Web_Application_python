from selenium import webdriver
from unittest import TestCase
from server import server
import sys


class TestPages(TestCase):
        def setUp(self):
            chromedriver = "./driver/chromedriver"
            self.browser = webdriver.Chrome(chromedriver)
            self.port = 2222
            server.start(self.port)

        def tearDown(self):
            self.browser.quit()

        def test_can_view_home_page(self):
            self.browser.get('http://127.0.0.1:{}'.format(self.port))

            self.assertIn(self.browser.title, 'Web App')
