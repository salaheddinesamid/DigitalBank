from django.test import TestCase
from ...utils.user_credentials_generator import generate_user_credentials


class UserCredentialsGeneratorTest(TestCase):

    def test_generate_user_credentials(self):
        first_name = "Salaheddine"
        last_name = "Samid"
        CIN = "T315730"

        expected = {
            "username": "SST315730",
            "password": "SAMIDSALAHEDDINET3157302026"
        }

        result = generate_user_credentials(
            first_name=first_name,
            last_name=last_name,
            CIN=CIN
        )
        self.assertEqual(expected, result)
