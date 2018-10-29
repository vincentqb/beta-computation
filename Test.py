import unittest
import pandas as pd
import DataProvider


# TODO Test each library and each function
# TODO Verify test coverage


# class TestBetasMethods(unittest.TestCase):


class TestDataProviderMethods(unittest.TestCase):

    def test_get_ref_security(self):
        start_date = "2013-10-01"
        end_date = "2018-10-01"
        df = DataProvider.get_reference_security(start_date, end_date)
        self.assertTrue(isinstance(df, pd.DataFrame))

    def test_get_one_random_securities(self):
        n = 1
        start_date = "2013-10-01"
        end_date = "2018-10-01"
        df = DataProvider.get_random_securities(n, start_date, end_date)
        self.assertTrue(isinstance(df, pd.DataFrame))

    def test_get_random_securities(self):
        n = 300
        start_date = "2013-10-01"
        end_date = "2018-10-01"
        df = DataProvider.get_random_securities(n, start_date, end_date)
        self.assertTrue(isinstance(df, pd.DataFrame))


if __name__ == '__main__':
    unittest.main()
