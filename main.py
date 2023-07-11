import dash
import plotly.graph_objs as go
import yfinance as yf
from dash import callback, dcc, html
from dash.dependencies import Input, Output

from fetch_data_service import fetch_yahoo_finance_data
from predicting_service import predict_coin_closing_price
from training_service import train_all_models

# fetch data to train
fetch_yahoo_finance_data()

# train models if not exists
train_all_models()

# render UI
app = dash.Dash()
app.layout = html.Div(
    [
        html.H1(
            "Closing price comparision dashboard",
            style={"textAlign": "center", "textTransform": "capitalize"},
        ),
        dcc.Tabs(
            id="tabs",
            children=[
                dcc.Tab(label="BTC-USD", value="btc_usd_tab"),
                dcc.Tab(label="ETH-USD", value="eth_usd_tab"),
                dcc.Tab(label="ADA-USD", value="ada_usd_tab"),
            ],
            value="btc_usd_tab",
        ),
        html.Div(id="tabs-content-graph"),
    ]
)


# define callbacks
@callback(
    Output("tabs-content-graph", "children"),
    Input("tabs", "value"),
)
def render_content(tab):
    data = []

    if tab == "btc_usd_tab":
        data = predict_coin_closing_price("BTC-USD")
    elif tab == "eth_usd_tab":
        data = predict_coin_closing_price("ETH-USD")
    elif tab == "eth_usd_tab":
        data = predict_coin_closing_price("ADA-USD")
    else:
        data = predict_coin_closing_price("BTC-USD")

    return html.Div(
        [
            dcc.Graph(
                id="graph",
                figure={
                    "data": [
                        go.Scatter(
                            x=data.index,
                            y=data["Close"],
                            name="Actual data",
                            mode="lines",
                        ),
                        go.Scatter(
                            x=data.index,
                            y=data["Predictions"],
                            name="Prediction data",
                            mode="lines",
                        ),
                    ],
                    "layout": go.Layout(
                        title="Closing price comparison",
                        xaxis={"title": "Datetime"},
                        yaxis={"title": "Closing Price (USD)"},
                    ),
                },
            )
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
