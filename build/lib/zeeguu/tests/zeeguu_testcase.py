# Mother of all Zeeguu testcases.
# Provides utility methods for logging in
# Makes sure that we are using the testing DB

import os
os.environ["ZEEGUU_TESTING"] = "True"
# It's important to set this up at the beginning of every test
# otherwise the tests will override the actual database!
# This is too fragile though... The moment I forget, this...

TEST_PASS='pass'
TEST_EMAIL='i@mir.lu'

import zeeguu
import unittest
import zeeguu.populate
# _without_rank
import zeeguu.model

class ZeeguuTestCase(unittest.TestCase):

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            login=True, #/login tests for the existence of "login" in this dict
            email=email,
            password=password
        ), follow_redirects=True)

    def i_login(self):
        self.login(TEST_EMAIL, TEST_PASS)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def get_session(self):
        self.i_login()
        rv = self.app.post('/session/'+TEST_EMAIL, data=dict(
            password=TEST_PASS
        ))

        return rv.data

    def in_session(self, url, other_args=[]):
        url_with_session = url + "?session=" + self.session
        for each in other_args:
            url_with_session += "&" + each
        print url_with_session
        return url_with_session


    def setUp(self):
        # zeeguu.app.config['TESTING'] = True
        self.app = zeeguu.app.test_client()
        zeeguu.populate.create_test_db()
        self.session = self.get_session()

    def tearDown(self):
        self.app = None
        self.session = None

    def api_get(self, test_data, formdata='None'):
        return self.app.get(self.in_session(test_data), data = formdata)

    def api_post(self, test_data, formdata='None'):
        return self.app.post(self.in_session(test_data), data = formdata)
