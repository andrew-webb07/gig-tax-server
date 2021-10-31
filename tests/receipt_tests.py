import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from gigtaxapi.models import Receipt, Musician

class ReceiptTests(APITestCase):
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
            "bio": "Love those receiptz!!"
        }
        response = self.client.post(url, data, format='json')
        # Convert JSON to a Python object
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        # Check if the response's status code is a 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(pk=1)

        musician = Musician.objects.get(pk=user.id)


    def test_create_receipt(self):
        """
        Ensure we can create a new receipt.
        """
        url = "/receipts"
        data = {
            "userId": 1,
            "businessName": "Guitar Center",
            "businessAddress": "29555 Northwestern Hwy, Southfield, MI, 48034",
            "description": "Double Bass Pedal",
            "date": "2021-07-01",
            "price": 379.99,
            "receiptNumber": "3331212121"
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the receipt was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["business_name"], data['businessName'])
        self.assertEqual(json_response["business_address"], data['businessAddress'])
        self.assertEqual(json_response["description"], data['description'])
        self.assertEqual(json_response["date"], data['date'])
        self.assertEqual(json_response["price"], data['price'])
        self.assertEqual(json_response["receipt_number"], data['receiptNumber'])

    def test_get_receipt(self):
        """
        Ensure we can get an existing receipt.
        """
        receipt = Receipt()
        receipt.musician_id = 1
        receipt.business_name = "Mars Music"
        receipt.business_address = "5555 Telegraph Road"
        receipt.description = "Tama Rockstar Receipt"
        receipt.date = "2003-07-01"
        receipt.price = 599.99
        receipt.receipt_number = "121212121"
        receipt.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/receipts/{receipt.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the receipt was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["business_name"], receipt.business_name)
        self.assertEqual(json_response["business_address"], receipt.business_address)
        self.assertEqual(json_response["description"], receipt.description)
        self.assertEqual(json_response["date"], receipt.date)
        self.assertEqual(json_response["price"], receipt.price)
        self.assertEqual(json_response["receipt_number"], receipt.receipt_number)

    def test_change_receipt(self):
        """
        Ensure we can change an existing receipt.
        """
        receipt = Receipt()
        receipt.musician_id = 1
        receipt.business_name = "Mars Music"
        receipt.business_address = "5555 Telegraph Road"
        receipt.description = "Tama Rockstar Receipt"
        receipt.date = "2003-07-01"
        receipt.price = 599.99
        receipt.receipt_number = "121212121"
        receipt.save()

        # DEFINE NEW PROPERTIES FOR RECEIPT
        data = {
            "userId": 1,
            "businessName": "Guitar Center",
            "businessAddress": "29555 Northwestern Hwy, Southfield, MI, 48034",
            "description": "Double Bass Pedal",
            "date": "2021-07-01",
            "price": 379.99,
            "receiptNumber": "3331212121"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/receipts/{receipt.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET RECEIPT AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/receipts/{receipt.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["business_name"], data["businessName"])
        self.assertEqual(json_response["business_address"], data['businessAddress'])
        self.assertEqual(json_response["description"], data['description'])
        self.assertEqual(json_response["date"], data['date'])
        self.assertEqual(json_response["price"], data['price'])
        self.assertEqual(json_response["receipt_number"], data['receiptNumber'])
        

    def test_delete_receipt(self):
        """
        Ensure we can delete an existing receipt.
        """
        receipt = Receipt()
        receipt.musician_id = 1
        receipt.business_name = "Mars Music"
        receipt.business_address = "5555 Telegraph Road"
        receipt.description = "Tama Rockstar Receipt"
        receipt.date = "2003-07-01"
        receipt.price = 599.99
        receipt.receipt_number = "121212121"
        receipt.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/receipts/{receipt.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET RECEIPT AGAIN TO VERIFY 404 response
        response = self.client.get(f"/receipts/{receipt.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)