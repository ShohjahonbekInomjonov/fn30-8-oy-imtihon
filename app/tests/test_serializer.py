from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from app.models import Menu, Restaurant
from app.serializers import MenuSerializer, RestaurantSerializer

class RestaurantSerializerTestCase(APITestCase):
    def setUp(self):
        self.res1 = Restaurant.objects.create(name="Turkish Cafe", address="Fergana", phone="+998916027449", email="turkish@gmail.com", is_active=True, category="caf")
        self.res2 = Restaurant.objects.create(name="English Cafe", address="Tashkent", phone="+998916027449", email="english@gmail.com", is_active=False, category="caf")
        self.res3 = Restaurant.objects.create(name="German Cafe", address="Andijan", phone="+998916027449", email="german@gmail.com", is_active=True, category="caf")

    def test_get(self):
        data = [
            {'id': self.res1.pk, 'likes': 0, 'dislikes': 0, 'comments': 0, 'menus': [], 'name': 'Turkish Cafe', 'description': None, 'address': 'Fergana', 'phone': '+998916027449', 'email': 'turkish@gmail.com', 'photo': None, 'is_active': True, 'category': 'caf'}, 
            {'id': self.res2.pk, 'likes': 0, 'dislikes': 0, 'comments': 0, 'menus': [], 'name': 'English Cafe', 'description': None, 'address': 'Tashkent', 'phone': '+998916027449', 'email': 'english@gmail.com', 'photo': None, 'is_active': False, 'category': 'caf'}, 
            {'id': self.res3.pk, 'likes': 0, 'dislikes': 0, 'comments': 0, 'menus': [], 'name': 'German Cafe', 'description': None, 'address': 'Andijan', 'phone': '+998916027449', 'email': 'german@gmail.com', 'photo': None, 'is_active': True, 'category': 'caf'}
        ]
        url = reverse('restaurant-list')

        serializer = RestaurantSerializer([self.res1, self.res2, self.res3], many=True)
        data2 = serializer.data
        # print(serializer.data)
        for item in data2:
            item.pop('created_at', None)
        # print(data2)
        self.assertEqual(data2, data)


class MenuSerializerTestCase(APITestCase):
    def setUp(self):
        self.res = Restaurant.objects.create(name="Turkish Cafe", address="Fergana", phone="+998916027449", email="turkish@gmail.com", is_active=True, category="caf")
        self.menu1 = Menu.objects.create(name="Breakfast", description="salom1", restaurant=self.res)
        self.menu2 = Menu.objects.create(name="Lunch", description="salom2", restaurant=self.res)
        self.menu3 = Menu.objects.create(name="Dinner", description="salom3", restaurant=self.res)
    
    def test_get(self):
        url = reverse('menu-list')

        data = [
            {'id': 1, 'dishes': [], 'restaurant_id': 1, 'name': 'Breakfast', 'description': 'salom1', 'restaurant': 1}, 
            {'id': 2, 'dishes': [], 'restaurant_id': 1, 'name': 'Lunch', 'description': 'salom2', 'restaurant': 1}, 
            {'id': 3, 'dishes': [], 'restaurant_id': 1, 'name': 'Dinner', 'description': 'salom3', 'restaurant': 1}
        ]

        serializer = MenuSerializer([self.menu1, self.menu2, self.menu3], many=True)

        # print(serializer.data)
        self.assertEqual(serializer.data, data)