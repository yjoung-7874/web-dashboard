import dash
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px
from utils import Header, make_dash_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))
df = pd.read_csv(DATA_PATH.joinpath("train.csv"))
df['Order Date']= pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date']= pd.to_datetime(df['Ship Date'], dayfirst=True)

# for Data Overview
columns = ['Customer ID', 'Sales', 'State','City', 'Country']
df_overview = df.columns.to_frame().T
df_overview = pd.concat([df_overview, df], ignore_index=True)
df_overview = df_overview.loc[:3, columns]
df_overview.iloc[-2, :] = "..."
df_overview.iloc[:, -2] = "..."

def create_layout(app):
  # Page layouts
  return html.Div([
    html.Div([Header(app)]),
    # page 1
    html.Div([
      # Row 3
      html.Div([
        html.Div([
          html.H5("Super Store Dataset"),
          html.Br([]),
          html.P(
            "\
            The superstore dataset is a simulation using a dashboard  where we can perform extensive \
            data analysis to predict the sales of the following days and to increase profits while \
            minimizing the losses. \
            \
            Based on the patterns that will show up in the dashboard, we can predict the subsequent patterns \
            and other characteristics of the data. \
            \
            These datasets are very useful when we are using economic data, weather data, stock prices, \
            and retail sales forecasting.",
            style={"color": "#000"},
            # className="row",
          ),
        ], className="product six columns", style={"height": "auto" }),
        html.Div([
          html.H6(["Data Overview"], className="subtitle padded"),
          html.Table(make_dash_table(df_overview)),
          html.P([
            html.Strong("Context"),
            html.P("Retail dataset of a global superstore for 4 years."),
            html.Strong("Shape"),
            html.P(f"{df.shape[0]} x {df.shape[1]}")
          ]),
        ], className="six columns", ),
      ], className="row", ),
      # Row 4
      html.Div([
        html.Div([
          html.H6("Sales Status Over Timeline", className="subtitle padded", ),
          html.Div([
            html.Div(
              dcc.Dropdown(
                df.loc[:, df.columns != 'Sales'].columns,
                'Segment',
                id='get_column'
              ), style={'width': '48%', 'display': 'inline-block'}
            ),
            html.Div(
              dcc.Dropdown(
                id='get_unique'
              ), style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
            )
          ]),
          dcc.Graph(id="date_graph"),
        ], className="six columns", ),
        html.Div([
          html.H6("Unique Values & Counts", className="subtitle padded", ),
          dcc.Dropdown(
            df.columns[(df.nunique() < 5)],
            'Segment',
            id='column_name'
          ),
          html.Br(),
          html.Div(id="unique_values"),
        ], className="six columns", ),
      ], className="row ", ),
      # Row 5
      html.Div([
        html.Div([
          html.H6(
            "Data Distribution",
            className="subtitle padded",
          ),
          html.Div([
            html.Div(
              dcc.Dropdown(
                df.columns,
                'Segment',
                id='xaxis-column'
              ), style={'width': '48%', 'display': 'inline-block'}
            ),
            html.Div(
              dcc.Dropdown(
                df.columns,
                'Category',
                id='yaxis-column'
              ), style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
            )
          ]),
          dcc.Graph(id="bar-graph",),
        ], className="columns", ),
      ], className="row", style={"margin-bottom": "35px"}, ),
    ], className="sub_page", ),
  ], className="page", )


@dash.callback(
  Output('get_unique', 'options'),
  Input('get_column', 'value'))
def set_options(selected_column):
  return [{'label': i, 'value': i} for i in df[selected_column].unique()]

@dash.callback(
  Output('get_unique', 'value'),
  Input('get_unique', 'options'))
def set_options_(available_options):
  return available_options[0]['value']

@dash.callback(
  Output('date_graph', 'figure'),
  Input('get_unique','value'),
  Input('get_column', 'value'))
def update_graph(unique_name, column_name):
  dff = df[df[column_name] == unique_name]
  dff.sort_values(by='Order Date', inplace=True)
  xaxis_column = 'Order Date'
  salesIdx = dff.columns.get_loc("Sales")
  array = []
  for i in range(dff.shape[0]):
    if i < dff.shape[0] and i >= dff.shape[0] - 10:
      array.append(dff.iloc[i-10:i, salesIdx].mean())
    else:
      array.append(dff.iloc[i:i+100, salesIdx].mean())

  dff['Mean'] = array
  fig = px.line(
    x=dff[xaxis_column],
    y=dff['Mean'],
    # size='Sales'
    # markers=True
  )
  fig.update_layout(
    autosize=True,
    title="",
    font={"family": "Raleway", "size": 10},
    height=200,
    width=340,
    hovermode="closest",
    legend={
      "x": -0.0277108433735,
      "y": -0.142606516291,
      "orientation": "h",
    },
    margin={
      "r": 20,
      "t": 20,
      "b": 20,
      "l": 50,
    },
    showlegend=True,
  )
  fig.update_xaxes(title=xaxis_column, autorange=True, 
                  showline=True,)
  fig.update_yaxes(title=f'Sales of {unique_name}', autorange=True,
                  showline=True, showgrid=True, zeroline=False)
  return fig

@dash.callback(
  Output('unique_values', 'children'),
  Input('column_name','value'))
def update_table(column_name):
  df_ = df[column_name].value_counts().to_frame().reset_index()
  df_vc = df_.rename(columns = {'index':'Values', column_name:'Counts'})
  df_result = df_vc.columns.to_frame().T
  df_result = pd.concat([df_result, df_vc], ignore_index=False)
  return html.Table(make_dash_table(df_result))

@dash.callback(
  Output('bar-graph', 'figure'),
  Input('xaxis-column', 'value'),
  Input('yaxis-column', 'value'))
def update_scatter_graph(xaxis_column_name, yaxis_column_name):
  fig = px.scatter(
    df,
    x=xaxis_column_name,
    y=yaxis_column_name,
    color='Sales',
    size="Sales",
  )
  fig.update_layout(
    autosize=False,
    bargap=False,
    font={"family": "Raleway", "size": 10},
    # height=200,
    # width=330,
    hovermode="closest",
    legend={
      "x": -0.0228945952895,
      "y": -0.189563896463,
      "orientation": "h",
      "yanchor": "top",
    },
    margin={ "r": 0, "t": 20, "b": 10, "l": 10, },
    title="",
    xaxis={'categoryorder':'category ascending'},
    showlegend=True,
  )
  fig.update_xaxes(title=xaxis_column_name, autorange=True, 
                  showline=True,)
  fig.update_yaxes(title=yaxis_column_name, autorange=True,
                  showline=True, showgrid=True, zeroline=False)
  return fig