import json
import multiprocessing
import unittest

from vkpm import login


class TestLogin(unittest.TestCase):
    def test_login_true(self):
        self.assertTrue(login)

    def test_login_false_password(self):
        username = 'Yarko'
        password = ' '
        self.assertFalse(login(username, password))

    def test_login_not_valid_data(self):
        username = 124512
        password = 'qwrfasfa'

        self.assertRaises(ValueError, login(username, password))


class TestCommit(unittest.TestCase):

    def test_get_all_commits(self):
        pass



if __name__ == '__main__':
    unittest.main()
