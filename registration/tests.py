from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
# Create your tests here.

class ProfileTestCase(TestCase):
    # Se prepara el test
    def setUp(self):
        User.objects.create_user('test','test@test.com','test1234')
    # Se ejecuta el test
    def test_profile_exist(self):
        exists = Profile.objects.filter(user__username='test').exists()
        self.assertEqual(exists, True)