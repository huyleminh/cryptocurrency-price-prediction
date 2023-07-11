import sys
from os import mkdir, path

import yfinance as yf

from coin_config import COIN_TO_TRAIN_CONFIG


def fetch_yahoo_finance_data():
    # ensure the data folder exists
    if not path.isdir("./data"):
        mkdir("./data")

    # Get data from yahoo finance and save to csv
    for config in COIN_TO_TRAIN_CONFIG.values():
        if not path.isfile("./data/{name:s}.csv".format(name=config["tickers"])):
            data = yf.download(
                tickers=config["tickers"],
                period=config["period"],
                interval=config["interval"],
            )

            data_file_location = "./data/{name:s}.csv"
            data.to_csv(data_file_location.format(name=config["tickers"]))
