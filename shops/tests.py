from django.test import TestCase, Client
from django.urls import reverse
from .models import Shop


class ShopViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse("shops:create-shop")
        # creating sample shops
        self.shop1 = Shop.objects.create(
            name="Shop 1", latitude=10.123, longitude=20.456
        )
        self.shop2 = Shop.objects.create(
            name="Shop 2", latitude=15.678, longitude=25.678
        )

    def test_create_shop_view(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shops/create_shop.html")

    def test_shop_list_view(self):
        url = reverse("shops:shop-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shops/shop_list.html")
        # assert that all shops are listed
        self.assertContains(response, self.shop1.name)
        self.assertContains(response, self.shop2.name)

    def test_update_shop_view(self):
        url = reverse("shops:update-shop", kwargs={"pk": self.shop1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shops/update_shop.html")

    def test_location_view(self):
        url = reverse("shops:location")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shops/location.html")

    def test_shop_within_distance_view(self):
        url = reverse("shops:shops-within-distance")
        response = self.client.post(
            url,
            {"latitude": 10.0, "longitude": 20.0, "distance": 100},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shops/shops.html")
        # assert that only nearby shops are returned
        self.assertContains(response, self.shop1.name)
        self.assertNotContains(response, self.shop2.name)
