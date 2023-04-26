from django.test import TestCase

from rest_framework.test import APITestCase

from .models import House, Amenity
from users.models import CustomUser
from categories.models import Category


# class TestAmenities(APITestCase):
#     USERNAME = "test_user"
#     PASSWORD = "1234"
#     NAME = "Amenity Name for Test"
#     DESCRIPTION = "Amenity Description for Test"
#     URL = "/api/v1/houses/amenities/"

#     def setUp(self) -> None:
#         user = CustomUser.objects.create_user(
#             username=self.USERNAME,
#         )
#         user.set_password(self.PASSWORD)
#         user.save()

#         self.client.login(
#             username=self.USERNAME,
#             password=self.PASSWORD,
#         )

#         for _ in range(10):
#             Amenity.objects.create(
#                 name=self.NAME,
#                 description=self.DESCRIPTION,
#             )

#     def test_all_amenities(self):
#         data = self.client.get(self.URL).json()
#         self.assertEqual(len(data), 10)

#     def test_create_amenity(self):
#         _name = "Amenity Name for Test"
#         _description = "Amenity Description for Test"

#         response = self.client.post(
#             path=self.URL,
#             data={
#                 "name": self.NAME,
#                 "description": self.DESCRIPTION,
#             },
#         )
#         data = response.json()

#         self.assertEqual(
#             response.status_code,
#             200,
#             "Not status code 200",
#         )
#         self.assertEqual(
#             data.get("name"),
#             _name,
#             "Description value doesn't match.",
#         )
#         self.assertEqual(
#             data.get("description"),
#             _description,
#             "Description value doesn't match.",
#         )

#         response = self.client.post(
#             path=self.URL,
#             data={
#                 "name": self.NAME,
#                 "description": self.DESCRIPTION,
#             },
#         )
#         data = response.json()

#         self.assertIn(
#             "name",
#             data,
#             "Not found in container",
#         )

#         self.assertEqual(
#             data.get("name"),
#             _name,
#             "Description value doesn't match.",
#         )

#     def tearDown(self) -> None:
#         return super().tearDown()


# class TestAmenity(APITestCase):
# USERNAME = "test_user"
# PASSWORD = "1234"
# NAME = "Amenity Name for Test"
# DESCRIPTION = "Amenity Description for Test"
# URL = "/api/v1/houses/amenities"

# def setUp(self):
#     user = CustomUser.objects.create_user(
#         username=self.USERNAME,
#     )
#     user.set_password(self.PASSWORD)
#     user.save()

#     self.client.login(
#         username=self.USERNAME,
#         password=self.PASSWORD,
#     )

#     Amenity.objects.create(
#         name=self.NAME,
#         description=self.DESCRIPTION,
#     )

# def test_get_amenity(self):
#     response = self.client.get(f"{self.URL}/1")
#     self.assertEqual(response.status_code, 200)

# def test_put_amenity(self):
#     pass

# def test_delete_amenity(self):
#     response = self.client.delete(f"{self.URL}/1")
#     self.assertEqual(response.status_code, 204)


class TestHouse(APITestCase):
    USERNAME = "test_user"
    PASSWORD = "1234"
    NAME = "House Name for Test"
    DESCRIPTION = "House Description for Test"
    URL = "/api/v1/houses/"

    def setUp(self):
        user = CustomUser.objects.create_user(
            username=self.USERNAME,
        )
        user.set_password(self.PASSWORD)
        user.save()
        self.user = user
        self.client.force_login(user)

        category = Category.objects.create(
            name="hotel",
            kind="houses",
        )

    def test_get_category(self):
        response = self.client.get("/api/v1/categories/")
        data = (response.json())[0]
        self.assertEqual(
            data.get("name"),
            "hotel",
        )

    def test_create_room(self):
        response = self.client.post(
            path=self.URL,
            data={
                "name": self.NAME,
                "description": self.DESCRIPTION,
                "price": 100,
                "rooms": 4,
                "toilets": 3,
                "address": "서울",
                "kind": "entire_place",
                "category": 1,
            },
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("name"), self.NAME)
