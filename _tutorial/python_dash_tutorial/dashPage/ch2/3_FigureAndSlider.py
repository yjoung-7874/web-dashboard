from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

app = Dash(__name__)

app.layout = html.Div([
  dcc.Graph(id='graph-with-slider'),
  dcc.Slider(
    df['lifeExp'].min(),
    df['lifeExp'].max(),
    step=500,
    value=df['lifeExp'].min(),
    marks={str(lifeExp): str(lifeExp) for lifeExp in df['lifeExp'].unique()},
    id='year-slider'
  )
])

@app.callback(
  Output('graph-with-slider', 'figure'),
  Input('year-slider', 'value'))
def update_figure(selected_year):
  filtered_df = df[df.lifeExp == selected_year]
  fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                    size="pop", color="continent", hover_name="country",
                    log_x=True, size_max=55)
  fig.update_layout(transition_duration=500)
  return fig


if __name__ == '__main__':
    app.run_server(debug=True)