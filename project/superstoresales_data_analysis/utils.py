from dash import dcc
from dash import html

def Header(app):
	return html.Div([
		get_header(app), 
		html.Br([]), 
		get_menu()
	])


def get_header(app):
  header = html.Div(
    [
      html.Br(),
      html.Div(
        html.A(
          html.Div(
            [
              html.Img(
                src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRUQVnAdc78g-U-Ei4gpDaHB621aVC71RhNA&usqp=CAU",
                style={"height": "100px", "width": "auto"},
                # className="two columns"
              ),  
              html.H3(
                "Sales Data Analisys Dashboard",
                style={ "height": "100px", "width":"700px", "padding-top": "25px" }
              )
            ], style={"height": "100px", "display": "flex" }
          ), href="/dash-financial-report/overview",
        ), className='row' 
      ),
      html.Hr(style={ "margin-top": "0px" }),
      html.Div(
        [
          html.Div(
            html.H5(
              "Data analysis for superstore sales"
            ), className="seven columns main-title",
          ),
        ], className="twelve columns", style={"padding-left": "0"},
      ),
    ], className="row"
  )
  return header


def get_menu():
	menu = html.Div(
		[
			dcc.Link(
				"DataSet",
				href="/dash-financial-report/overview",
				className="tab first",
				# style={'margin-right': '20px', 'margin-left': '20px'}
			),
			dcc.Link(
				"Analysis",
				href="/dash-financial-report/price-performance",
				className="tab",
				# style={'margin-right': '20px', 'margin-left': '20px'}
			),
			dcc.Link(
				"News & Reviews",
				href="/dash-financial-report/news-and-reviews",
				className="tab",
				# style={'margin-right': '20px', 'margin-left': '20px'}
			),
		], className="row all-tabs", style={"border-left": "5px solid #2fc1de"}
	)
	
	return menu


def make_dash_table(df):
	""" Return a dash definition of an HTML table for a Pandas dataframe """
	table = []
	for index, row in df.iterrows():
		html_row = []
		for i in range(len(row)):
			html_row.append(html.Td([row[i]]))
		table.append(html.Tr(html_row))
	return table
