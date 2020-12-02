import unittest

from django.utils import timezone

from .forms import NewListingForm
from .models import Listing
from django.template import Context, Template

app_name = 'listing'


class YourTestClass(unittest.TestCase):
    def test_validate_listing_false(self):
        # Test with normal fields
        print("Method: test_validate_Listing_false.")
        listings_db = list(Listing.cs_3240_listings.all())  # [0].split(", ")

        listing_data = {
            'uid': 'at8gb',
            'course': 'BME',
            'section': 4747,
            'lecture': 'IN_PERSON',
            'timezone': 'Los Angeles',
            'language': 'Armenian',
            'professor': 'Scott T. Action',
            'major': 'Anthropology',
            'pub_date': timezone.now(),
            'comment': 'This is a valid form',
            'study_time': timezone.now(),
        }
        form = NewListingForm(data=listing_data)
        print("\n\nuid: ", form.data['uid'], "\n")
        print("course: ", form.data['course'], "\n")
        print("section: ", form.data['section'], "\n")
        print("lecture: ", form.data['lecture'], "\n")
        print("timezone: ", form.data['timezone'], "\n")
        print("language: ", form.data['language'], "\n")
        print("professor: ", form.data['professor'], "\n")
        print("major: ", form.data['major'], "\n")
        print("pub_date: ", form.data['pub_date'], "\n")
        print("comment: ", form.data['comment'], "\n\n")
        print("study_time: ", form.data['study_time'], "\n")
        print("\t\tCS 3240 Manager: ", listings_db, "\n\n")
        print("\t\temail: ", listings_db)  # [0].split(", "), "\n\n")
        self.assertTrue(form.data['section'] == 4747)
        self.assertFalse(form.is_valid())


class YourTestClass(unittest.TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def render_context(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

        template = Template("Welcome to the {{ app_name }} app.")

        context = Context({"app_name": "Study Buddy©"})
        template.render(context)


#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#         self.assertFalse(False)
#
#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         self.assertFalse(False)
#
#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)

# def test_was_published_recently_with_future_listing(self):
#     """
#     was_published_recently() returns False for questions whose pub_date
#     is in the future.
#     """
#     time = timezone.now() + datetime.timedelta(days=30)
#     future_listing = NewListingForm(pub_date=time)
#     self.assertIs(future_listing.was_published_recently(), True)
#

if __name__ == '__main__':
    unittest.main()
