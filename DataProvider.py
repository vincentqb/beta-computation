import configparser
import pandas_datareader as pdr
import pandas as pd


CONFIG_NAME = "config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_NAME)

API_KEY = config["TIINGO"]["API_KEY"]
VALUE_COL = config["TIINGO"]["VALUE_COL"]
REFERENCE_SECURITY = config["MAIN"]["REFERENCE_SECURITY"]
DATA_STORE = config["MAIN"]["DATA_STORE"]


def get_securities(codes, start_date, end_date, backup=True):
    """
    Get given security for given date range.

    :param codes: list of securities to get
    :param start_date: start date
    :param end_date: end date
    :return: data frame with given security
    """

    df = pdr.get_data_tiingo(codes, api_key=API_KEY)
    if backup: df.to_hdf(DATA_STORE,'table', append=True)

    df = df[VALUE_COL]
    date = df.index.get_level_values('date')
    df[(date >= start_date) & (date <= end_date)]
    return df


def load_securities():
    return pd.read_hdf(DATA_STORE, "table")[VALUE_COL]


def get_codes(n):
    """
    Get n random security names from database.

    :param n: number of random securities to get
    :return: list of n security names
    """

    # exchanges = ["BSE", "BEX", "BOX", "CBOE", "CBOT", "CME", "CHX", "ISE", "MS4X", "NSX", "PHLX", "NYSE", "NYSE ARCA", "NYSE EUROTEXT", "NASDAQ", "AMEX"]
    exchanges = ["NYSE", "NASDAQ", "AMEX"]

    stocks = pdr.tiingo.get_tiingo_symbols()
    stocks = stocks[
        (stocks["priceCurrency"] == "USD")
        & (stocks["assetType"] == "Stock")
        & (stocks["exchange"].isin(exchanges))
        # & (stocks["startDate"] <= "2013-10-01")
        # & (stocks["endDate"] >= "2018-10-01")
    ].dropna().sample(n)

    return list(stocks["ticker"])


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
    return get_securities(codes, start_date, end_date)


def get_reference_security(start_date, end_date):

    # Get securities
    return get_securities([REFERENCE_SECURITY], start_date, end_date).to_frame()[VALUE_COL]
