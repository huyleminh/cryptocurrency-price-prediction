from os import mkdir, path

import numpy as np
import pandas as pd
from keras.layers import LSTM, Dense, Dropout
from keras.models import Sequential, load_model
from sklearn.preprocessing import MinMaxScaler

from coin_config import COIN_TO_TRAIN_CONFIG


def prepare_train_data(final_data):
    # train_data = final_data[0:2000, :]
    train_data = final_data[:, :]

    min_max_scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = min_max_scaler.fit_transform(final_data)

    x_train_data, y_train_data = [], []

    lstm_window_size = 60

    for i in range(lstm_window_size, len(train_data)):
        x_train_data.append(scaled_data[i - lstm_window_size : i, 0])
        y_train_data.append(scaled_data[i, 0])

    x_train_data, y_train_data = np.array(x_train_data), np.array(y_train_data)

    x_train_data = np.reshape(
        x_train_data, (x_train_data.shape[0], x_train_data.shape[1], 1)
    )

    return (x_train_data, y_train_data)


def build_lstm_model(x_train_data, y_train_data):
    lstm_model = Sequential()
    lstm_model.add(
        LSTM(units=50, return_sequences=True, input_shape=(x_train_data.shape[1], 1))
    )
    lstm_model.add(LSTM(units=50))
    lstm_model.add(Dense(1))

    lstm_model.compile(loss="mean_squared_error", optimizer="adam")
    lstm_model.fit(x_train_data, y_train_data, epochs=1, batch_size=1, verbose=2)

    return lstm_model


def filter_data_by_columns(data, columns):
    # Sort the dataset on date time and filter "Datetime" and "Close" columns:
    sorted_data = data.sort_index(ascending=True, axis=0)

    # Initialize new dataset from the origin
    new_dataset = pd.DataFrame(index=range(0, len(data)), columns=columns)

    for i in range(0, len(sorted_data)):
        new_dataset["Datetime"][i] = sorted_data["Datetime"][i]
        new_dataset["Close"][i] = sorted_data["Close"][i]

    # Normalize the new filtered dataset
    new_dataset.index = new_dataset.Datetime
    new_dataset.drop("Datetime", axis=1, inplace=True)

    return new_dataset


def save_lstm_model_to_csv(lstm_model, filename):
    # Save the LSTM model
    if not path.isdir("./models"):
        mkdir("./models")

    lstm_model.save("./models/" + filename)


def train_all_models():
    for config in COIN_TO_TRAIN_CONFIG.values():
        # try loading old models
        if not path.isfile("./models/{name:s}.keras".format(name=config["tickers"])):
            train_model_by_coin_pair(config["tickers"])


def train_model_by_coin_pair(coin_pair_name):
    # read the dataset
    root_dataset = pd.read_csv("./data/{name:s}.csv".format(name=coin_pair_name))
    root_dataset.index = root_dataset["Datetime"]

    new_dataset = filter_data_by_columns(root_dataset, ["Datetime", "Close"])

    # Get clean data
    final_dataset = new_dataset.values

    # prepare data
    x_train_data, y_train_data = prepare_train_data(final_dataset)

    # start training
    model = build_lstm_model(x_train_data, y_train_data)

    # save as csv
    save_lstm_model_to_csv(model, coin_pair_name + ".keras")


if __name__ == "__main__":
    train_all_models()
