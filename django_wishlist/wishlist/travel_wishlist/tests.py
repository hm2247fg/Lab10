from django.test import TestCase
from django.urls import reverse

from .models import Place
# Create your tests here.


# Test class for the home page
class TestHomePage(TestCase):

    # Test that the home page shows an empty list message for an empty database
    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist')


# Test class for the visited page
class TestVisitedPage(TestCase):

    # def test_visited_page_shows_empty_list_message_for_empty_database(self):
    #     response = self.client.get(reverse('places_visited'))
    #     self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
    #     self.assertContains(response, 'You have not visited any places yet')

    # Test that the visited page shows a message when no places have been visited
    def test_visited_page_shows_no_places_visited_message(self):
        # Get the URL of the visited page
        visited_page_url = reverse('places_visited')
        # Send a GET request to the visited page URL
        response = self.client.get(visited_page_url)
        # Check if the response contains the expected message
        self.assertContains(response, 'You have not visited any places yet')


# Test class for the wishlist
class TestWishList(TestCase):
    fixtures = ['test_places']

    # Test that the wishlist page contains only not visited places
    def test_viewing_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')


# Test class for the visited list
class TestVisitedList(TestCase):
    fixtures = ['test_places.json']

    # def test_viewing_places_visited_shows_visited_places(self):
    #     response = self.client.get(reverse('places_visited'))
    #     self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
    #
    #     self.assertNotContains(response, 'Tokyo')
    #     self.assertNotContains(response, 'New York')
    #     self.assertContains(response, 'San Francisco')
    #     self.assertContains(response, 'Moab')

    # Test that only visited places are displayed on the visited page
    def test_only_visited_places_displayed(self):
        # Set up visited and not visited places
        visited_places = Place.objects.filter(visited=True)
        not_visited_places = Place.objects.filter(visited=False)
        # Get the URL of the visited page
        visited_page_url = reverse('places_visited')
        # Send a GET request to the visited page URL
        response = self.client.get(visited_page_url)
        # Check if visited places are displayed
        for place in visited_places:
            self.assertContains(response, place.name)
        # Check if not visited places are not displayed
        for place in not_visited_places:
            self.assertNotContains(response, place.name)


# Test class for adding a new place
class TestAddNewPlace(TestCase):

    # Test adding a new unvisited place to the wishlist
    def test_add_new_unvisited_place_to_wishlist(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}

        response = self.client.post(add_place_url, new_place_data, follow=True)
        # Check correct template was used
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # What data was used to populate the template?
        response_places = response.context['places']
        # Should be 1 item
        self.assertEqual(1, len(response_places))
        tokyo_response = response_places[0]

        # Expect this data to be in the database. Use get() to get data with
        # the values expected. Will throw an exception if no data, or more than
        # one row, matches. Remember throwing an exception will cause this test to fail
        tokyo_in_database = Place.objects.get(name='Tokyo', visited=False)

        # Is the data used to render the template, the same as the data in the database?
        self.assertEqual(tokyo_in_database, tokyo_response)

        # And add another place - still works?
        response = self.client.post(reverse('place_list'), {'name': 'Yosemite', 'visited': False}, follow=True)

        # Check correct template was used
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # What data was used to populate the template?
        response_places = response.context['places']
        # Should be 2 items
        self.assertEqual(2, len(response_places))

        # Expect this data to be in the database. Use get() to get data with
        # the values expected. Will throw an exception if no data, or more than
        # one row, matches. Remember throwing an exception will cause this test to fail
        place_in_database = Place.objects.get(name='Yosemite', visited=False)
        place_in_database = Place.objects.get(name='Tokyo', visited=False)

        places_in_database = Place.objects.all()  # Get all data

        # Is the data used to render the template, the same as the data in the database?
        self.assertCountEqual(list(places_in_database), list(response_places))

    # Test adding a new visited place to the wishlist
    def test_add_new_visited_place_to_wishlist(self):
        response = self.client.post(reverse('place_list'), {'name': 'Tokyo', 'visited': True}, follow=True)

        # Check correct template was used
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # What data was used to populate the template?
        response_places = response.context['places']

        # Should be 0 items - have not added any un-visited places
        self.assertEqual(0, len(response_places))

        # Expect this data to be in the database. Use get() to get data with
        # the values expected. Will throw an exception if no data, or more than
        # one row, matches. Remember throwing an exception will cause this test to fail
        place_in_database = Place.objects.get(name='Tokyo', visited=True)


# Test class for visiting a place
class TestVisitPlace(TestCase):
    fixtures = ['test_places.json']

    # Test visiting a place
    def test_visit_place(self):
        # visit place pk = 2,  New York
        visit_place_url = reverse('place_was_visited', args=(2,))
        response = self.client.post(visit_place_url, follow=True)

        # Check correct template was used
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # no New York in the response
        self.assertNotContains(response, 'New York')

        # Is New York visited?
        new_york = Place.objects.get(pk=2)

        self.assertTrue(new_york.visited)

    # Test visiting a non-existent place
    def test_visit_non_existent_place(self):
        # visit place with pk = 200, this PK is not in the fixtures
        visit_place_url = reverse('place_was_visited', args=(200,))
        response = self.client.post(visit_place_url, follow=True)
        self.assertEqual(404, response.status_code)  # not found