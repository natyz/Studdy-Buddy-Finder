import unittest

from profile_page.forms import UserProfileForm
from contact_form.forms import ContactForm
import home.views as home_views
from django.test import Client
from profile_page.models import UserProfile
from listing.models import Listing, GroupMember, Group, Membership

class ListingTestCase(unittest.TestCase):
    def test_listingspage_1(self):
        c = Client()
        response = c.get('/listings')
        self.assertEqual(response.status_code, 200)

    def test_listingmodel_1(self):
        list = Listing.get_all_listings.update_or_create(uid="UserA", section=1000, study_time="2020-12-19T16:39:57-08:00")
        self.assertTrue(Listing.get_all_listings.filter(uid="UserA").exists())
        Listing.get_all_listings.filter(uid="UserA").delete()

    def test_listingmodel_2(self):
        list = Listing.get_all_listings.update_or_create(uid="UserB", zid='11111111111', section=1000, study_time="2020-12-19T16:39:57-08:00")
        self.assertTrue(Listing.get_all_listings.filter(uid="UserB").exists())
        self.assertTrue(Listing.get_all_listings.filter(zid='11111111111').exists())
        Listing.get_all_listings.filter(uid="UserB").delete()

    def test_listingmodel_3(self):
        list = Listing.get_all_listings.update_or_create(uid="UserC", zid='11111111112', major="Computer Science", member2="User2", section=1030, study_time="2020-12-19T16:39:57-08:00")
        self.assertTrue(Listing.get_all_listings.filter(uid="UserC").exists())
        self.assertTrue(Listing.get_all_listings.filter(zid='11111111112').exists())
        Listing.get_all_listings.filter(uid="UserC").delete()

    def test_groupmember_1(self):
        gm1 = GroupMember.objects.update_or_create(id=1111111155, group=1)
        self.assertTrue(GroupMember.objects.filter(id=1111111155).exists())
        GroupMember.objects.filter(id=1111111155).delete()
        self.assertFalse(GroupMember.objects.filter(id=1111111155).exists())

    def test_group_1(self):
        g1 = Group.objects.update_or_create(id=123333333, join_group=False)
        self.assertTrue(Group.objects.filter(id=123333333).exists())
        Group.objects.filter(id=123333333).delete()
        self.assertFalse(Group.objects.filter(id=123333333).exists())

    def test_membership_1(self):
        gm1 = GroupMember.objects.update_or_create(id=1111111158, group=123333333)
        g1 = Group.objects.update_or_create(id=123333333, join_group=False)
        m1 = Membership.objects.update_or_create(date_joined="2020-11-19", group_id=123333333, person_id=1111111157)
        self.assertTrue(Membership.objects.filter(group_id=123333333))
        GroupMember.objects.filter(id=1111111158).delete()
        Membership.objects.filter(group_id=123333333).delete()
        Group.objects.filter(id=12333333).delete()
        self.assertFalse(GroupMember.objects.filter(id=11111111578).exists())
        self.assertFalse(Membership.objects.filter(group_id=123333333))

class ProfileTestCase(unittest.TestCase):
    def test_validate_model_1(self):
        # Test with normal fields
        user = UserProfile.objects.update_or_create(nickname="User1")
        self.assertTrue(UserProfile.objects.filter(nickname="User1").exists())
        self.assertFalse(UserProfile.objects.filter(nickname="N").exists())

    def test_validate_model_2(self):
        user = UserProfile.objects.update_or_create(nickname="User2", image="pic.jpg")
        self.assertTrue(UserProfile.objects.filter(nickname="User2").exists())

    def test_validate_form_3(self):
        user = UserProfile.objects.update_or_create(nickname="User3", year=2020, image="pic.jpg")
        self.assertTrue(UserProfile.objects.filter(nickname="User3").exists())

    def test_validate_form_4(self):
        user = UserProfile.objects.update_or_create(nickname="User4", year=2020, image="pic.jpg", zoom_id="1111111111")
        self.assertTrue(UserProfile.objects.filter(nickname="User4").exists())
        self.assertTrue(UserProfile.objects.filter(zoom_id="1111111111").exists())

    def test_validate_form_5(self):
        # Test with a wrong field
        profile_data = {
            'nickname': 'Josh',
            'major': 'something that isnt a major',
            'year': '2023',
            'zoom_id': '000-000-0000',
        }
        form = UserProfileForm(data=profile_data)
        self.assertFalse(form.is_valid())

    def test_validate_form_6(self):
        # Test with a different but correct field
        profile_data = {
            'nickname': 'Josh',
            'major': 'Global Studies',
            'year': 2023,
            'zoom_id': '000-000-0000',
        }
        form = UserProfileForm(data=profile_data)
        self.assertTrue(form.is_valid())

    def test_validate_form_7(self):
        # Test with a wrong field
        profile_data = {
            'nickname': 'Josh',
            'major': 'Global Studies',
            'bio': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
                   'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
                   'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
                   'aaa',  # greater than 250 characters
            'zoom_id': '000-000-0000',
        }
        form = UserProfileForm(data=profile_data)
        self.assertFalse(form.is_valid())

    def test_validate_form_8(self):
        # Test with a wrong field
        profile_data = {
            'nickname': 'Josh',
            'major': 'Global Studies',
            'bio': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
                   'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'zoom_id': '000-000-0000',
        }  # fewer than 250 characters for bio
        form = UserProfileForm(data=profile_data)
        self.assertTrue(form.is_valid())

    def test_validate_form_9(self):
        # Test with a working field that uses certain non-alphanumeric characters
        profile_data = {
            'nickname': '_Josh _',
            'major': 'Global Studies',
            'zoom_id': '000-000-0000',
        }  # fewer than 250 characters for bio
        form = UserProfileForm(data=profile_data)
        self.assertTrue(form.is_valid())

    def test_validate_form_10(self):
        # Test with a non-working field
        profile_data = {
            'nickname': '_Josh _*',
            'major': 'Global Studies',
            'zoom_id': '000-000-0000'
        }  # fewer than 250 characters for bio
        form = UserProfileForm(data=profile_data)
        self.assertFalse(form.is_valid())

    def test_validate_form_11(self):
        # Testing an emptyish profile
        profile_data = {
            'nickname': '',
            'major': '',
            'year': '',
            'bio': '',
            'zoom_id': '000-000-0000',
            'class_1': '',
            'class_2': '',
        }  # more classes would probably be redundant
        form = UserProfileForm(data=profile_data)
        self.assertTrue(form.is_valid())

    def test_validate_form_12(self):
        # Testing different order of class entry
        profile_data = {
            'nickname': '',
            'major': '',
            'year': '',
            'bio': '',
            'zoom_id': '123-456-7890',
            'class_1': '',
            'class_2': 'CS3240',
        }  # doesn't matter in what order the fields of the classes are entered
        form = UserProfileForm(data=profile_data)
        self.assertTrue(form.is_valid())

    def test_validate_form_11(self):
        # Testing an emptyish profile
        profile_data = {
            'nickname': '',
            'major': '',
            'year': '',
            'bio': '',
            'zoom_id': '000-000-00000',
            'class_1': '',
            'class_2': '',
        }  # more classes would probably be redundant
        form = UserProfileForm(data=profile_data)
        self.assertFalse(form.is_valid())

class ContactUsTestCase(unittest.TestCase):
    def test_validate_form_1(self):
        # Test with working field
        contact_data = {
            'name' : 'Bill',
            'email' :'billgogo@gmail.com',
            'message': 'Help',
        }
        form =ContactForm(data=contact_data)
        self.assertTrue(form.is_valid())

    def test_validate_form_2(self):
        # Test with invalid email
        contact_data = {
            'name': 'Bill',
            'email': 'billgoggmail.com',
            'message': 'Help',
        }
        form = ContactForm(data=contact_data)
        self.assertTrue(form.is_valid())

    def test_validate_form_3(self):

        # Test with invalid email
        contact_data = {
            'name': 'Bill',
            'email': 'billgoggmail.com',
            'message': '',
        }
        form = ContactForm(data=contact_data)
        self.assertFalse(form.is_valid())

    def test_contactpage_1(self):
        c = Client()
        response = c.get('/contact')
        self.assertEqual(response.status_code, 200)


class HomepageTest(unittest.TestCase):
    def test_homepage_1(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_2(self):
        c = Client()
        response = c.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        c = Client()
        response = c.get('/login')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
