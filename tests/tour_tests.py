import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from gigtaxapi.models import Tour, Musician

class TourTests(APITestCase):
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
            "bio": "Love those tourz!!"
        }
        response = self.client.post(url, data, format='json')
        # Convert JSON to a Python object
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        # Check if the response's status code is a 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(pk=1)

        musician = Musician.objects.get(pk=user.id)


    def test_create_tour(self):
        """
        Ensure we can create a new tour.
        """
        url = "/tours"
        data = {
            "userId": 1,
            "artist": "Reyna Roberts",
            "tourDepartureAddress": "4726 Traders Way, Thompson's Station, TN 37179",
            "tourDescription": "Country Tour",
            "numberOfGigs": 12,
            "perDiem": 20,
            "travelDays": 5,
            "travelDayPay": 100,
            "dateStart": "2021-07-01",
            "dateEnd": "2021-07-17",
            "tourGigPay": 200,
            "mileage": 10
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the tour was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["artist"], data["artist"])
        self.assertEqual(json_response["tour_departure_address"], data['tourDepartureAddress'])
        self.assertEqual(json_response["tour_description"], data['tourDescription'])
        self.assertEqual(json_response["number_of_gigs"], data['numberOfGigs'])
        self.assertEqual(json_response["per_diem"], data['perDiem'])
        self.assertEqual(json_response["travel_days"], data['travelDays'])
        self.assertEqual(json_response["travel_day_pay"], data['travelDayPay'])
        self.assertEqual(json_response["date_start"], data['dateStart'])
        self.assertEqual(json_response["date_end"], data['dateEnd'])
        self.assertEqual(json_response["tour_gig_pay"], data['tourGigPay'])
        self.assertEqual(json_response["mileage"], data['mileage'])
        

    def test_get_tour(self):
        """
        Ensure we can get an existing tour.
        """
        tour = Tour()
        tour.musician_id = 1
        tour.artist = "Syndrome of Fire"
        tour.tour_departure_address = "Kroger"
        tour.tour_description = "Rock Tour"
        tour.number_of_gigs = 10
        tour.per_diem = 15
        tour.travel_days = 4
        tour.travel_day_pay = 50
        tour.date_start = "2017-09-01"
        tour.date_end = "2017-09-14"
        tour.tour_gig_pay = 100
        tour.mileage = 15
        tour.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/tours/{tour.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the tour was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["artist"], tour.artist)
        self.assertEqual(json_response["tour_departure_address"], tour.tour_departure_address)
        self.assertEqual(json_response["tour_description"], tour.tour_description)
        self.assertEqual(json_response["number_of_gigs"], tour.number_of_gigs)
        self.assertEqual(json_response["per_diem"], tour.per_diem)
        self.assertEqual(json_response["travel_days"], tour.travel_days)
        self.assertEqual(json_response["travel_day_pay"], tour.travel_day_pay)
        self.assertEqual(json_response["date_start"], tour.date_start)
        self.assertEqual(json_response["date_end"], tour.date_end)
        self.assertEqual(json_response["tour_gig_pay"], tour.tour_gig_pay)
        self.assertEqual(json_response["mileage"], tour.mileage)

    def test_change_tour(self):
        """
        Ensure we can change an existing tour.
        """
        tour = Tour()
        tour.musician_id = 1
        tour.artist = "Syndrome of Fire"
        tour.tour_departure_address = "Kroger"
        tour.tour_description = "Rock Tour"
        tour.number_of_gigs = 10
        tour.per_diem = 15
        tour.travel_days = 4
        tour.travel_day_pay = 50
        tour.date_start = "2017-09-01"
        tour.date_end = "2017-09-14"
        tour.tour_gig_pay = 100
        tour.mileage = 15
        tour.save()

        # DEFINE NEW PROPERTIES FOR TOUR
        data = {
            "userId": 1,
            "artist": "Reyna Roberts",
            "tourDepartureAddress": "4726 Traders Way, Thompson's Station, TN 37179",
            "tourDescription": "Country Tour",
            "numberOfGigs": 12,
            "perDiem": 20,
            "travelDays": 5,
            "travelDayPay": 100,
            "dateStart": "2021-07-01",
            "dateEnd": "2021-07-17",
            "tourGigPay": 200,
            "mileage": 10
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/tours/{tour.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET TOUR AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/tours/{tour.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["artist"], data["artist"])
        self.assertEqual(json_response["tour_departure_address"], data['tourDepartureAddress'])
        self.assertEqual(json_response["tour_description"], data['tourDescription'])
        self.assertEqual(json_response["number_of_gigs"], data['numberOfGigs'])
        self.assertEqual(json_response["per_diem"], data['perDiem'])
        self.assertEqual(json_response["travel_days"], data['travelDays'])
        self.assertEqual(json_response["travel_day_pay"], data['travelDayPay'])
        self.assertEqual(json_response["date_start"], data['dateStart'])
        self.assertEqual(json_response["date_end"], data['dateEnd'])
        self.assertEqual(json_response["tour_gig_pay"], data['tourGigPay'])
        self.assertEqual(json_response["mileage"], data['mileage'])
        

    def test_delete_tour(self):
        """
        Ensure we can delete an existing tour.
        """
        tour = Tour()
        tour.musician_id = 1
        tour.artist = "Syndrome of Fire"
        tour.tour_departure_address = "Kroger"
        tour.tour_description = "Rock Tour"
        tour.number_of_gigs = 10
        tour.per_diem = 15
        tour.travel_days = 4
        tour.travel_day_pay = 50
        tour.date_start = "2017-09-01"
        tour.date_end = "2017-09-14"
        tour.tour_gig_pay = 100
        tour.mileage = 15
        tour.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/tours/{tour.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET TOUR AGAIN TO VERIFY 404 response
        response = self.client.get(f"/tours/{tour.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)