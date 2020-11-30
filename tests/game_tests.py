import json
from rest_framework import status
from rest_framework.test import APITestCase
from gamerraterapi.models import Game


class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "first_name": "Steve",
            "last_name": "Brownlee"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_game(self):
        """ Ensure a game can be made"""

        url = "/games"
        data = {
            "title": "Clue",
            "description": "Fun Family Game",
            "numberOfPlayers": 4,
            "yearReleased": 1991,
            "estimatedTime": 20,
            "ageRecommendation": 12,
            "designer": "Cool Guy Bob",
            "user": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response= self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["title"], "Clue")
        self.assertEqual(json_response["description"], "Fun Family Game")
        self.assertEqual(json_response["numberOfPlayers"], 4)
        self.assertEqual(json_response["yearReleased"], 1991)
        self.assertEqual(json_response["estimatedTime"], 20)
        self.assertEqual(json_response["ageRecommendation"], 12)
        self.assertEqual(json_response["designer"], "Cool Guy Bob")