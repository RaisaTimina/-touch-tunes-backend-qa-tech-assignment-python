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
    dataList = [0, 1, 10, 100, "", " ", "tomato", "tomato1", "tomATo", "ToMato2", "To Ma To", "tO Ma To16",
                "password1234", "tomato?", "2tomatoS!"]

    @classmethod
    def setUpClass(self):
        auth = "Discogs key={}, secret={}".format(self.key, self.secret)
        self.headers = {
            "Content-Type": self.content_type,
            "Authorization": auth
        }

    def test_basic_response(self):
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers)

        self.assertEqual(res.status_code, 200)

    def test_both_bad_credentials_random(self):
        badAuth = "Discogs key={}, secret={}".format(random_string(), random_string())
        self.badHeaders = {
            "Content-Type": self.content_type,
            "Authorization": badAuth
        }
        res = requests.get("{}/search".format(self.discog_url), headers=self.badHeaders)

        self.assertEqual(res.status_code, 401)

    def test_bad_key_random(self):
        badKeyAuth = "Discogs key={}, secret={}".format(random_string(), self.secret)
        self.badKeyHeaders = {
            "Content-Type": self.content_type,
            "Authorization": badKeyAuth
        }

        res = requests.get("{}/search".format(self.discog_url), headers=self.badKeyHeaders)

        self.assertEqual(res.status_code, 401)

    def test_bad_secret_random(self):
        badSecretAuth = "Discogs key={}, secret={}".format(self.key, random_string())
        badSecretHeaders = {
            "Content-Type": self.content_type,
            "Authorization": badSecretAuth
        }
        res = requests.get("{}/search".format(self.discog_url), headers=badSecretHeaders)
        self.assertEqual(res.status_code, 401)

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
                time.sleep(60/60)

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

    #         If no limit specified, we return default number of record per pages.
    def test_limit_per_page_not_specified(self):
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers)

        paginationResponse = res.json()
        paginationArray = paginationResponse['pagination']
        paginationPerPage = paginationArray['per_page']

        resultsResponse = res.json()
        resultsObject = resultsResponse['results']
        self.assertEqual(paginationPerPage, len(resultsObject))

    # run through a for looop? try strings, decimals, etc
    #     - If a specific limit is specified, the api must return the requested number of record per pages.
    def test_limit_per_page_specified2(self):
        value = random_number_under_limit()
        res = requests.get("{}/search?per_page={}".format(self.discog_url, value),
                           headers=self.headers)

        resultsResponse = res.json()
        resultsObject = resultsResponse['results']
        self.assertEqual(value, len(resultsObject))

    def test_limit_per_page_specified(self):
        for value in range(1, 101):
            with self.subTest(value=value):
                res = requests.get("{}/search?per_page={}".format(self.discog_url, value), headers=self.headers)

                resultsResponse = res.json()
                resultsObject = resultsResponse['results']
                self.assertEqual(value, len(resultsObject))
                time.sleep(60 / 60) #due to the requests limit (60/minute) had to slow the process down

    #     - The api will return a maximun number of result per pages, even if we provide a large limit value.
    def test_pages_over_limit(self):
        res = requests.get("{}/search?per_page={}".format(self.discog_url, random_number_over_limit()),
                           headers=self.headers)
        resultsResponse = res.json()
        resultsObject = resultsResponse['results']
        print(len(resultsObject))
        self.assertLessEqual(len(resultsObject), 100)


if __name__ == '__main__':
    unittest.main()
