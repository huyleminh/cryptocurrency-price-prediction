import numpy as np
import pandas as pd
import yfinance as yf
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler


def predict_coin_closing_price(coin_pair_name):
    # read the dataset
    root_dataset = yf.download(tickers=coin_pair_name, period="72h", interval="1m")

    # add column
    root_dataset.insert(0, "Datetime", root_dataset.index.values, False)

    # Sort the dataset on date time and filter "Datetime" and "Close" columns:
    sorted_data = root_dataset.sort_index(ascending=True, axis=0)
    new_dataset = pd.DataFrame(
        index=range(0, len(root_dataset)), columns=["Datetime", "Close"]
    )

    for i in range(0, len(sorted_data)):
        new_dataset["Datetime"][i] = sorted_data["Datetime"][i]
        new_dataset["Close"][i] = sorted_data["Close"][i]

    # Normalize the new filtered dataset
    new_dataset.index = new_dataset.Datetime
    new_dataset.drop("Datetime", axis=1, inplace=True)

    final_dataset = new_dataset.values

    valid = final_dataset[2000:, :]
    # valid = final_dataset[-1000:]

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(final_dataset)

    # load existing model instead of training again
    model = load_model("./models/{name:s}.keras".format(name=coin_pair_name))

    inputs = new_dataset[len(new_dataset) - len(valid) - 60 :].values
    inputs = inputs.reshape(-1, 1)
    inputs = scaler.transform(inputs)

    X_test = []
    for i in range(60, inputs.shape[0]):
        X_test.append(inputs[i - 60 : i, 0])
    X_test = np.array(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    closing_price = model.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)

    # Visualize the predicted stock costs with actual stock costs
    valid = new_dataset[2000:]
    # valid = new_dataset[-1000:]
    valid["Predictions"] = closing_price

    return valid
