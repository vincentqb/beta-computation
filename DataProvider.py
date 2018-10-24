import urllib.request
import configparser
import pandas as pd
import quandl
from functools import reduce


CONFIG_NAME = "config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_NAME)

API_KEY = config["QUANDL"]["API_KEY"]
DB_NAME = config["QUANDL"]["DB_NAME"]
VALUE_COL = config["QUANDL"]["VALUE_COL"]

quandl.ApiConfig.api_key = API_KEY


def get_security(code, start_date, end_date):
    """
    Get given security for given date range.

    :param code: security to get
    :param start_date: start date
    :param end_date: end date
    :return: data frame with given security
    """
    code_long = DB_NAME + "/" + code
    return quandl.get(
        code_long,
        start_date=start_date,
        end_date=end_date,
        returns="pandas"
    )[VALUE_COL].to_frame(name=code)


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


def get_securities(n, start_date, end_date):
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

    dfs = []

    for code in codes:
        df = get_security(code, start_date, end_date)
        dfs.append(df)

    return reduce(
            lambda left, right: pd.merge(left, right, on="Date"),
            dfs
    )
