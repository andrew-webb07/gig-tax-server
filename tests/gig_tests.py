import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from gigtaxapi.models import Gig, Musician

class GigTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gigz!!"
        }
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(pk=1)

        musician = Musician.objects.get(pk=user.id)


    def test_create_gig(self):
        """
        Ensure we can create a new gig.
        """
        url = "/gigs"
        data = {
            "userId": 1,
            "artist": "Reyna Roberts",
            "locationName": "The Barnyard",
            "locationAddress": "Sharpsburg, KY",
            "gigDescription": "Country Show",
            "date": "2021-07-08",
            "gigPay": 200,
            "mileage": 10
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the gig was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["artist"], data["artist"])
        self.assertEqual(json_response["location_name"], data['locationName'])
        self.assertEqual(json_response["location_address"], data['locationAddress'])
        self.assertEqual(json_response["gig_description"], data['gigDescription'])
        self.assertEqual(json_response["date"], data['date'])
        self.assertEqual(json_response["gig_pay"], data['gigPay'])
        self.assertEqual(json_response["mileage"], data['mileage'])
        

    def test_get_gig(self):
        """
        Ensure we can get an existing gig.
        """
        gig = Gig()
        gig.musician_id = 1
        gig.artist = "Syndrome of Fire"
        gig.location_name = "Exit In"
        gig.location_address = "Nashville,TN"
        gig.gig_description = "Rock Show"
        gig.date = "2017-06-30"
        gig.gig_pay = 100
        gig.mileage = 52
        gig.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/gigs/{gig.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the gig was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["artist"], gig.artist)
        self.assertEqual(json_response["location_name"], gig.location_name)
        self.assertEqual(json_response["location_address"], gig.location_address)
        self.assertEqual(json_response["gig_description"], gig.gig_description)
        self.assertEqual(json_response["date"], gig.date)
        self.assertEqual(json_response["gig_pay"], gig.gig_pay)
        self.assertEqual(json_response["mileage"], gig.mileage)

    def test_change_gig(self):
        """
        Ensure we can change an existing gig.
        """
        gig = Gig()
        gig.musician_id = 1
        gig.artist = "Syndrome of Fire"
        gig.location_name = "Exit In"
        gig.location_address = "Nashville,TN"
        gig.gig_description = "Rock Show"
        gig.date = "2017-06-30"
        gig.gig_pay = 100
        gig.mileage = 52
        gig.save()

        # DEFINE NEW PROPERTIES FOR GIG
        data = {
            "userId": 1,
            "artist": "Reyna Roberts",
            "locationName": "The Barnyard",
            "locationAddress": "Sharpsburg, KY",
            "gigDescription": "Country Show",
            "date": "2021-07-08",
            "gigPay": 200,
            "mileage": 10
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/gigs/{gig.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GIG AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/gigs/{gig.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["artist"], data["artist"])
        self.assertEqual(json_response["location_name"], data['locationName'])
        self.assertEqual(json_response["location_address"], data['locationAddress'])
        self.assertEqual(json_response["gig_description"], data['gigDescription'])
        self.assertEqual(json_response["date"], data['date'])
        self.assertEqual(json_response["gig_pay"], data['gigPay'])
        self.assertEqual(json_response["mileage"], data['mileage'])
        

    def test_delete_gig(self):
        """
        Ensure we can delete an existing gig.
        """
        gig = Gig()
        gig.musician_id = 1
        gig.artist = "Syndrome of Fire"
        gig.location_name = "Exit In"
        gig.location_address = "Nashville,TN"
        gig.gig_description = "Rock Show"
        gig.date = "2017-06-30"
        gig.gig_pay = 100
        gig.mileage = 52
        gig.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/gigs/{gig.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GIG AGAIN TO VERIFY 404 response
        response = self.client.get(f"/gigs/{gig.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)