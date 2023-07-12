# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# data handling
df = pd.DataFrame({
  "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
  "Amount": [4, 1, 2, 2, 4, 5],
  "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

# plotly > figure
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# Dash html layout
app.layout = html.Div(children=[
  html.H1(children='Hello Dash'),

  html.Div(children='''
    Dash: A web application framework for your data.
  '''),
  # dcc Graph
  dcc.Graph(
    id='example-graph',
    figure=fig
  )
])

# run server
if __name__ == '__main__':
  app.run_server(debug=True)