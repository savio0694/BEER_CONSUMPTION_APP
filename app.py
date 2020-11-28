import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_table
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
import dash_bootstrap_components as dbc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
server = app.server
#loading  the data,cleaning already done in the ipython notebook
beer_data=pd.read_csv('beer.csv')
beer_data=beer_data.drop('Unnamed: 0',axis=1)
beer_data=beer_data.round(2)
reg_data=beer_data.iloc[:,[2,3,4]]
reg_target=beer_data.iloc[:,[6]]

X_train, X_test, y_train, y_test = train_test_split(reg_data,reg_target,random_state=1,shuffle=True,test_size=0.1)
Lreg = Ridge(alpha=0.5)
Lreg.fit(X_train, y_train)



app.layout = html.Div(children=[
dbc.Container([

dbc.Row([

    dbc.Col([

dbc.NavbarSimple(
    brand="PREDICTING BEER CONSUMPTION",
    brand_href="#",
    color="success",
    dark=True,
)])


]),

    dbc.Row([

    dbc.Col([
html.H5("CHOOSE DISTRIBUTION"),

            dcc.Dropdown(
                id='hist-choice',
                options=[

                    {'label': 'rain', 'value':'precipitation' },
                    {'label': 'min_temp', 'value':'min_temp'},
                    {'label': 'mean_temp', 'value':'mean_temp'}

                ],
                value='min_temp'
            ),
            dcc.Graph(
                id='hist1')

            ]),

dbc.Col(
dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in beer_data.columns],
    data=beer_data.to_dict('records'),
    page_size=15,
     style_as_list_view=True,
     style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }]
)
      )


]),

    dbc.Row([
dbc.Col([

dbc.Jumbotron([
        html.H5('CHOOSE MIN_TEMP'),
        dcc.Slider(
        id='min_temp_slider',
        min=beer_data['min_temp'].min(),
        max=beer_data['min_temp'].max(),

        marks={str(temp): str(temp) for temp in [10,15,20,25,30,35]},
        step=1,
        value=5
    ),

    html.H5('CHOOSE MAX_TEMP'),
    dcc.Slider(
id='max_temp_slider',
min=beer_data['max_temp'].min(),
max=beer_data['max_temp'].max(),

marks={str(temp): str(temp) for temp in [10,15,20,25,30,35]},
step=1,
value=5
),

html.H5('CHOOSE PRECIPITATION'),
    dcc.Slider(
id='precipitation_slider',
min=beer_data['precipitation'].min(),
max=beer_data['precipitation'].max(),

marks={str(temp): str(temp) for temp in [1,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95]},
step=1,
value=5
)
])

]),


dbc.Col([
dbc.Card(
    dbc.CardBody(
html.H3(id='output-text')
))
])


])
],fluid=True)
])



@app.callback(
    Output('hist1', 'figure'),
    [Input('hist-choice', 'value')])
def update_figure(selected):


    fig = px.histogram(beer_data,x=selected,template='simple_white')

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output("output-text", "children"),
    [Input("max_temp_slider", "value"), Input("min_temp_slider", "value"),Input("precipitation_slider", "value")],
)
def update_output(max_temp_slider, min_temp_slider,precipitation_slider):
    data = {'max_temp': [max_temp_slider], 'min_temp': [min_temp_slider],'precipitation': [precipitation_slider]}
    df = pd.DataFrame(data, columns=['max_temp', 'min_temp', 'precipitation'])
    ypred=Lreg.predict(df)
    return u'Min temperature is {} , Max temperature is {} , precipitation is {}'.format(min_temp_slider,max_temp_slider,precipitation_slider) +' '+' the predicted value of beer consumption based on ridge regession model is %d'%(ypred)


if __name__ == '__main__':
    app.run_server(debug=True)
