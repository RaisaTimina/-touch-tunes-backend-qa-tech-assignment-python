import unittest
import time

import requests
import random
import string


def random_string():
    randomPasswordString = (''.join((random.choice(string.ascii_letters) for i in range(16))))
    return randomPasswordString


def random_number_under_limit():
    randomNumberUnder = (random.randint(1, 100))
    return randomNumberUnder


def random_number_over_limit():
    randomNumberOver = (random.randint(101, 201))
    return randomNumberOver


class TestDiscogs(unittest.TestCase):
    key = "QxAZxYyroemyEvusEPHC "
    secret = "sNbIErqcWrSRWmiPeAJXXHZUGsWMGQwx"
    discog_url = "https://api.discogs.com/database"
    content_type = "application/x-www-form-urlencoded"
    dataList = [0, 1, 10, 100, "1 ", "1 !", "!@", "", " ", "tomato", "tomato1", "tomATo", "ToMato2", "To Ma To",
                "tO Ma To16", "TOMATOOO", "TOMATO3", "TOMATO$23", "TOMATO ", "password1234", "tomato?", "2tomatoS!"]

    @classmethod
    def setUpClass(self):
        auth = "Discogs key={}, secret={}".format(self.key, self.secret)
        self.headers = {
            "Content-Type": self.content_type,
            "Authorization": auth
        }

    # check if connection works when both key and secret are correct
    def test_basic_response(self):
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers)

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.json())

    # check if we can get to an id successfully when both key and secret are correct
    def test_search_successful_when_authorized(self):
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers)

        resultsResponse = res.json()
        resultsObject = resultsResponse['results']
        for i in resultsObject:
            self.assertIsNotNone(i["id"])
            time.sleep(60 / 60)

        self.assertEqual(res.status_code, 200)

    # check if get response when both KEY and SECRET are NOT correct
    # check with random string
    def test_both_bad_credentials_random(self):
        badAuth = "Discogs key={}, secret={}".format(random_string(), random_string())
        self.badHeaders = {
            "Content-Type": self.content_type,
            "Authorization": badAuth
        }
        res = requests.get("{}/search".format(self.discog_url), headers=self.badHeaders)

        self.assertEqual(res.status_code, 401)

    # check with an array of hardcoded possible passwords
    def test_bad_key_and_bad_secret(self):
        for value in self.dataList:
            with self.subTest(value=value):
                badSecretAuth = "Discogs key={}, secret={}".format(value, value)
                badSecretHeaders = {
                    "Content-Type": self.content_type,
                    "Authorization": badSecretAuth
                }
                res = requests.get("{}/search".format(self.discog_url), headers=badSecretHeaders)
                self.assertEqual(res.status_code, 401)
                time.sleep(60 / 60)

    # check if get response when KEY is NOT correct
    # check with random string
    def test_bad_key_only_random(self):
        badKeyAuth = "Discogs key={}, secret={}".format(random_string(), self.secret)
        self.badKeyHeaders = {
            "Content-Type": self.content_type,
            "Authorization": badKeyAuth
        }

        res = requests.get("{}/search".format(self.discog_url), headers=self.badKeyHeaders)

        self.assertEqual(res.status_code, 401)

    # check with an array of hardcoded possible passwords
    def test_bad_key_only(self):
        for value in self.dataList:
            with self.subTest(value=value):
                badSecretAuth = "Discogs key={}, secret={}".format(value, self.secret)
                badSecretHeaders = {
                    "Content-Type": self.content_type,
                    "Authorization": badSecretAuth
                }
                res = requests.get("{}/search".format(self.discog_url), headers=badSecretHeaders)
                self.assertEqual(res.status_code, 401)
                time.sleep(60 / 60)

    # check if get response when SECRET is NOT correct
    # check with random string
    def test_bad_secret_only_random(self):
        badSecretAuth = "Discogs key={}, secret={}".format(self.key, random_string())
        badSecretHeaders = {
            "Content-Type": self.content_type,
            "Authorization": badSecretAuth
        }
        res = requests.get("{}/search".format(self.discog_url), headers=badSecretHeaders)
        self.assertEqual(res.status_code, 401)

    # check with an array of hardcoded possible passwords
    def test_bad_secret_only(self):
        for value in self.dataList:
            with self.subTest(value=value):
                badSecretAuth = "Discogs key={}, secret={}".format(self.key, value)
                badSecretHeaders = {
                    "Content-Type": self.content_type,
                    "Authorization": badSecretAuth
                }
                res = requests.get("{}/search".format(self.discog_url), headers=badSecretHeaders)
                self.assertEqual(res.status_code, 401)
                time.sleep(60 / 60)

    # check if returns default number of record per pages when LIMIT is NOT specified
    def test_limit_per_page_not_specified(self):
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers)

        paginationResponse = res.json()
        paginationArray = paginationResponse['pagination']
        paginationPerPage = paginationArray['per_page']

        resultsResponse = res.json()
        resultsObject = resultsResponse['results']
        self.assertEqual(paginationPerPage, len(resultsObject))

    # check api returns the requested number of records per pages when LIMIT specified
    # check requested number of records per page matches the RANDOMly generated limit
    def test_limit_per_page_specified_random(self):
        value = random_number_under_limit()
        res = requests.get("{}/search?per_page={}".format(self.discog_url, value),
                           headers=self.headers)

        resultsResponse = res.json()
        resultsObject = resultsResponse['results']
        self.assertEqual(value, len(resultsObject))

    # check requested number of records per page matches GIVEN limit from 1 to 100
    def test_limit_per_page_specified_from_1_to_100(self):
        for value in range(1, 101):
            with self.subTest(value=value):
                res = requests.get("{}/search?per_page={}".format(self.discog_url, value), headers=self.headers)

                resultsResponse = res.json()
                resultsObject = resultsResponse['results']
                self.assertEqual(value, len(resultsObject))
                time.sleep(60 / 60)  # due to the requests limit (60/minute) had to slow the process down

    # check the number of records per page will stay at the maximum (100) if given a number above RANDOMly generated
    def test_pages_over_limit_random(self):
        res = requests.get("{}/search?per_page={}".format(self.discog_url, random_number_over_limit()),
                           headers=self.headers)
        resultsResponse = res.json()
        resultsObject = resultsResponse['results']
        print(len(resultsObject))
        self.assertLessEqual(len(resultsObject), 100)


if __name__ == '__main__':
    unittest.main()
