from unittest import TestCase

from selenium import webdriver


class TestPages(TestCase):
        def setUp(self):
            chromedriver = "../driver/chromedriver"
            self.browser = webdriver.Chrome(chromedriver)
            self.port = 8050
            self.url = 'http://localhost:8050'

        def tearDown(self):
            self.browser.quit()

        def test_can_view_home_page(self):
            self.browser.get(url=self.url)

            self.assertIn(self.browser.title, 'Web App')
