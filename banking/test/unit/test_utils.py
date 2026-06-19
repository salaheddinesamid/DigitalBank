from django.test import TestCase
from ...utils.user_credentials_generator import generate_user_credentials
from ...utils.account_number_generator import generate_account_number

mocked_user = {
    "id": 1,
    "first_name": "Salaheddine",
    "last_name": "Samid",
    "CIN": "T315730"
}


class UserCredentialsGeneratorTest(TestCase):

    def test_generate_user_credentials(self):
        expected = {
            "username": "SST315730",
            "password": "SAMIDSALAHEDDINET3157302026"
        }

        result = generate_user_credentials(
            first_name=mocked_user['first_name'],
            last_name=mocked_user['last_name'],
            CIN=mocked_user['CIN']
        )
        self.assertEqual(expected, result)


class AccountNumberGeneratorTest(TestCase):

    def test_generate_account_number(self):
        results = generate_account_number(
            id=mocked_user['id'],
            first_name=mocked_user['first_name'],
            last_name=mocked_user['last_name'],
            CIN=mocked_user['CIN']
        )

        self.assertEqual(results, "DGB1SST315730")


class TransferLimitUtilsTest(TestCase):
    pass


class TestGetIpAddress(TestCase):
    pass
