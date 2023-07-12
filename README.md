# Cryptocurrency Price Prediction

## General
- This project is a homework of the new technologies course in University of Science HCM.
- The main purpose is studying!

## Prerequisites
- Python 3.11.x
- Pip 23.1.2

## Usage
- Install all package
```
pip install -r requirements.txt
```

- Run the app
```
python main.py
```

- Open: http://127.0.0.1:8050/

## Notes
- The data folder keeps old datasets which are prepared for training process. So if you want to refresh them, then run:

```
python fetch_data_service.py
```

- The models folder keep old lstm models, run the following script in order to refresh:

```
python training_service.py
```

## Reference
- [Stock Price Prediction – Machine Learning Project in Python](https://data-flair.training/blogs/stock-price-prediction-machine-learning-project-in-python/)

- [Python: How to Get Live Cryptocurrency Data(Less Than 0.1-Second Lag).](https://medium.com/analytics-vidhya/python-how-to-get-bitcoin-data-in-real-time-less-than-1-second-lag-38772da43740)
