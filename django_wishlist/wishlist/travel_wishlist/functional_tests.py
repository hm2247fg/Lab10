from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from django.test import LiveServerTestCase

from .models import Place


class TitleTest(LiveServerTestCase):
    # Test case to check if the title is shown on the home page
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_title_shown_on_home_page(self):
        # Load the home page
        self.selenium.get(self.live_server_url)
        # Check if the title contains 'Travel Wishlist'
        self.assertIn(self.selenium.title, 'Travel Wishlist')


class AddPlacesTests(LiveServerTestCase):
    fixtures = ['test_places']

    # Test case to add a new place
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_add_new_place(self):
        # Load the home page
        self.selenium.get(self.live_server_url)
        # Find input text box and enter place name
        input_name = self.selenium.find_element_by_id('id_name')
        input_name.send_keys('Denver')
        # Find the add button and click it
        add_button = self.selenium.find_element_by_id('add-new-place')
        add_button.click()
        # Expect new element to appear on page with the text 'Denver'
        denver = self.selenium.find_element_by_id('place-name-5')
        self.assertEqual('Denver', denver.text)
        # Assert Denver is in the page source
        self.assertIn('Denver', self.selenium.page_source)
        # Assert places from test_places are on page
        self.assertIn('Tokyo', self.selenium.page_source)
        self.assertIn('New York', self.selenium.page_source)
        # Verify the database is updated
        denver_db = Place.objects.get(pk=5)
        self.assertEqual('Denver', denver_db.name)
        self.assertFalse(denver_db.visited)


class EditPlacesTests(LiveServerTestCase):
    fixtures = ['test_places']

    # Test case to mark a place as visited
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_mark_place_as_visited(self):
        # Load the home page
        self.selenium.get(self.live_server_url)
        # Find visited button and click it
        visited_button = self.selenium.find_element(By.ID, 'visited-button-2')
        visited_button.click()
        # Wait for the page to reload
        wait = WebDriverWait(self.selenium, 3)
        wait.until(EC.invisibility_of_element_located((By.ID, 'place-name-2')))
        # Assert Tokyo is still on page
        self.assertIn('Tokyo', self.selenium.page_source)
        # Assert New York is not on page
        self.assertNotIn('New York', self.selenium.page_source)
        # Load visited page
        self.selenium.get(self.live_server_url + '/visited')
        # Assert New York is on the visited page
        self.assertIn('New York', self.selenium.page_source)
        # Verify the database is updated - New York visited is True
        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)


class PageContentTests(LiveServerTestCase):
    fixtures = ['test_places']

    # Test case to check the content of the home page
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_get_home_page_list_of_places(self):
        # Load the home page
        self.selenium.get(self.live_server_url)
        # Assert places from test_places are on page
        self.assertIn('Tokyo', self.selenium.page_source)
        self.assertIn('New York', self.selenium.page_source)
        # Assert San Francisco and Moab are not on page
        self.assertNotIn('San Francisco', self.selenium.page_source)
        self.assertNotIn('Moab', self.selenium.page_source)

    # Test case to check the content of the visited page
    def test_get_list_of_visited_places(self):
        # Load the visited page
        self.selenium.get(self.live_server_url + '/visited')
        # Assert Tokyo and New York are not on visited page
        self.assertNotIn('Tokyo', self.selenium.page_source)
        self.assertNotIn('New York', self.selenium.page_source)
        # Assert San Francisco and Moab are on visited page
        self.assertIn('San Francisco', self.selenium.page_source)
        self.assertIn('Moab', self.selenium.page_source)