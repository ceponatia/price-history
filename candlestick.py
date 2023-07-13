import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('price_history.csv')

fig = go.Figure(data=[go.Candlestick(x=df['time'],
                                     open=df['price'],
                                     high=df['price'],
                                     low=df['price'],
                                     close=df['price'])])

fig.write_html('candlestick_chart.html')