from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@sheracore.com',
            password='test123'
            )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@sheracore.com',
            password='test123',
            name='Test user full name'
            )

    def test_user_listed(self):
        """ Test that users are listed on user page """
        # Changes in url in future the reverse automaticly been updated
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        """assrtContains is a django custom assertion
        that will check our response of cantain a certain item
        response li http response with 200 """
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """ Test that the user edit page works """
        # /admin/core/user/id
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
