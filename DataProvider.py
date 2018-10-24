import os
import urllib.request
import configparser
import pandas as pd
from pandas_datareader import data
from functools import reduce


CONFIG_NAME = "config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_NAME)

API_KEY = config["QUANDL"]["API_KEY"]
DB_NAME = config["QUANDL"]["DB_NAME"]
VALUE_COL = config["QUANDL"]["VALUE_COL"]

os.environ["QUANDL_API_KEY"] = API_KEY


def get_spy(start_date, end_date):
    """
    Get SPY for given date range.

    :param start_date: start date
    :param end_date: end date
    :return: data frame with given security
    """

    # NOTE SPY is not returned when requested alone
    dummy_ind = "AAPL"
    ind = "SPY"
    return (
            get_securities([dummy_ind, ind], start_date, end_date)
            .drop(dummy_ind, axis=1)
    )


def get_securities(codes, start_date, end_date):
    """
    Get given security for given date range.

    :param codes: list of securities to get
    :param start_date: start date
    :param end_date: end date
    :return: data frame with given security
    """

    return data.DataReader(codes, 'quandl', start_date, end_date)[VALUE_COL]


def get_codes(n):
    """
    Get n random security names from database.

    :param n: number of random securities to get
    :return: list of n security names
    """

    filename_input = (
            "https://www.quandl.com/api/v3/databases/"
            + DB_NAME
            + "/metadata?api_key="
            + API_KEY
    )
    filename_output = DB_NAME + ".zip"

    urllib.request.urlretrieve(filename_input, filename_output)

    df_codes = pd.read_csv(filename_output)

    # FIXME This may not cover small, medium, large cap.
    return list(df_codes["code"].sample(n))


def get_random_securities(n, start_date, end_date):
    """
    Get n random securities for given date range.

    :param n: number of random securities to get
    :param start_date: start date
    :param end_date: end date
    :return: data frame with n securities
    """

    # Get random codes from database

    codes = get_codes(n)

    # Get securities

    return get_security(codes, start_date, end_date)
