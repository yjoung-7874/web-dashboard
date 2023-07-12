# -*- coding: utf-8 -*-
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
# from mainDash import app

from pages import (
  overview,
  pricePerformance,
  portfolioManagement,
  feesMins,
  distributions,
  newsReviews,
)
app = dash.Dash(
  __name__, 
  meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.config.suppress_callback_exceptions=True

app.title = "SuperStore Sales Report"
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
  [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
  if pathname == "/dash-financial-report/price-performance":
    return pricePerformance.create_layout(app)
  elif pathname == "/dash-financial-report/news-and-reviews":
    return newsReviews.create_layout(app)
  else:
    return overview.create_layout(app)

if __name__ == "__main__":
  app.run_server(debug=True)
