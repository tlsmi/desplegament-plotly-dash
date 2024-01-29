import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
import seaborn as sns
from dash.dependencies import Input, Output
from flask import Flask


server = Flask(__name__)

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/healthexp.csv')

sns.set(style="whitegrid")

df1 = df.drop('Life_Expectancy',axis=1)
df2 = df.drop('Spending_USD',axis=1)

# Initialize the app
app = dash.Dash(server=server,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# Crear opciones para los dropdowns de años y países
available_countries = sorted(df1['Country'].unique())

# Establecer valores predeterminados para el rango de años
min_year = df1['Year'].min()
max_year = df1['Year'].max()

#
titulo1 = f'Spending_USD a lo largo de los años por país'
titulo2 = f'Distribución de Spending_USD por país en el año seleccionado'

countries = ['Germany','France','Great Britain','Japan','USA','Canada']




# Estilo de fondo para el cuerpo de la página
body_style = {
    'margin': 0, 
    'padding': 0
    }

app.layout =  html.Div(children=[
    html.H1(
        children='Expectativa de la Vida',
        style={
            'textAlign': 'center',
            'background': '#000000',
            'color': '#FFFFFF',
            'margin-bottom': '10px',
            'padding': '10px' 
        }
    ),

    html.H3(
        children='Determina el Año',
        style={
                'textAlign':'center',
                'color': '#14213D'
        }
    ),
    
   # RangeSlider para seleccionar un rango de años
    dcc.RangeSlider(
        id='year-slider',
        min=min_year,
        max=max_year,
        marks={str(year): str(year) for year in range(min_year, max_year+1)},
        value=[min_year, max_year],  # Valor predeterminado,º
        step=1
    ),
    dbc.Row([
        dbc.Col(html.H3(children='Selecciona los países',
        style={
                'textAlign':'center',
                'color': '#14213D',
                'margin-top': 5
        }),width=12)
    ]),
    dbc.Row(
        dbc.Col(
            # RadioItems para seleccionar entre 'Spending_USD' y 'Life_Expectancy'
            dcc.RadioItems(
                id='metric-radio',
                options=[
                    {'label': 'Gasto en USD', 'value': 'Spending_USD'},
                    {'label': 'Expectativa de vida', 'value': 'Life_Expectancy'}
                ],
                value='Spending_USD',  # Valor predeterminado
                labelStyle={'display': 'inline-block', 'margin-right': '20%'},
                style={
                    'text-align':'center',
                    'margin-left':'17%'
                    }
            ), 
            width=12, align='center'
        )
    ),
    dbc.Row([
        dbc.Col(
            html.H3(
                id='titulo1',
                style={
                    'textAlign':'center',
                    'color': '#FCA311',
                    'margin-top': 5
                }
            )
            , width=6
        ),
        dbc.Col(html.H3(id='titulo2',
        style={
                'textAlign':'center',
                'color': '#FCA311',
                'margin-top': 5
        }),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='line-plot'),width=6),
        dbc.Col(dcc.Graph(id='pie-chart'),width=6)
    ]),
    dbc.Row([
        dbc.Col(
            html.H3(
                id='titulo3',
                style={
                    'textAlign':'center',
                    'color': '#FCA311',
                    'margin-top': 5
                }
            )
            , width=6
        ),
        dbc.Col(html.H3(children='Clicka en la Primera Tabla para ver la comparativa en ese año contra el Mundo',
        style={
                'textAlign':'center',
                'color': '#FCA311',
                'margin-top': 5
        }),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='ratio-line-plot'),width=6),
dbc.Col([
    dbc.Row(
        dbc.Col([
            html.H3(
                id='clicked_year',
                style={
                    'textAlign': 'center',
                    'background-color': '#E5E5E5',  # Color de fondo
                    'margin': '10px',  # Margen exterior
                    'padding': '10px'  # Relleno interno
                }
            ),
        ])
    ),
    dbc.Row([
        dbc.Col([
            html.H3(
                id='clicked_country',
                style={
                    'textAlign': 'center',
                    'background-color': '#E5E5E5',
                    'margin': '10px',
                    'padding': '10px'
                }
            ),
        ]),
        dbc.Col([
            html.H3(
                id='spending',
                style={
                    'textAlign': 'center',
                    'background-color': '#E5E5E5',
                    'margin': '10px',
                    'padding': '10px'
                }
            ),
            html.H3(
                id='healthexp',
                style={
                    'textAlign': 'center',
                    'background-color': '#E5E5E5',
                    'margin': '10px',
                    'padding': '10px'
                }
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H3(
                id='mean_world',
                style={
                    'textAlign': 'center',
                    'background-color': '#E5E5E5',
                    'margin': '10px',
                    'padding': '10px'
                }
            ),
        ]),
        dbc.Col([
            html.H3(
                id='world_spending',
                style={
                    'textAlign': 'center',
                    'background-color': '#E5E5E5',
                    'margin': '10px',
                    'padding': '10px'
                }
            ),
            html.H3(
                id='world_healthexp',
                style={
                    'textAlign': 'center',
                    'background-color': '#E5E5E5',
                    'margin': '10px',
                    'padding': '10px'
                }
            )
        ])
    ])
], width=6)

    ])
], style=body_style)
    

@app.callback(
    [Output('line-plot', 'figure'),
     Output('pie-chart', 'figure'),
     Output('ratio-line-plot', 'figure'),
     Output('titulo1', 'children'),
     Output('titulo2', 'children'),
     Output('titulo3', 'children')],
    [Input('year-slider', 'value'),
     Input('metric-radio', 'value')]
)

def update_line_plot(selected_years, selected_metric):
    if (selected_metric == 'Spending_USD'):
        dfGraph = df1
        titulo1 = 'Gasto a lo largo de los años por país'
        titulo2 = 'Distribución del Gasto por país en el año seleccionado'
        titulo3 = 'Ratio Gasto País sobre la Media a lo largo de los años'
    else: 
        dfGraph = df2
        titulo1 = 'Expectativa de Vida a lo largo de los años por país'
        titulo2 = 'Distribución de la Expectativa de Vida por país en el año seleccionado'
        titulo3 = 'Ratio de Expectativa de Vida País sobre la Media a lo largo de los años'
     
    # Filtrar el DataFrame según los años y países seleccionados
    filtered_df = dfGraph[(dfGraph['Year'] >= selected_years[0]) & (dfGraph['Year'] <= selected_years[1])]
    
    if (selected_metric == 'Spending_USD'):
        # Crear DataFrame para el ratio Spending_USD de cada país sobre la media
        groupedYear = pd.DataFrame(filtered_df.groupby(by='Year')['Spending_USD'].mean())
        groupedYear = pd.merge(filtered_df, groupedYear, on='Year', how='left', suffixes=('', '_grouped'))
        groupedYear['ratio'] = groupedYear['Spending_USD'] / groupedYear['Spending_USD_grouped']
    else:
        # Crear DataFrame para el ratio Spending_USD de cada país sobre la media
        groupedYear = pd.DataFrame(filtered_df.groupby(by='Year')['Life_Expectancy'].mean())
        groupedYear = pd.merge(filtered_df, groupedYear, on='Year', how='left', suffixes=('', '_grouped'))
        groupedYear['ratio'] = groupedYear['Life_Expectancy'] / groupedYear['Life_Expectancy_grouped']

    # Gráfico de líneas
    line_fig = px.line(filtered_df, x='Year', y=selected_metric, color='Country', line_group='Country',
                       labels={selected_metric: selected_metric},
                    #    title=f'{selected_metric} a lo largo de los años por país'
                       )
        
        # Gráfico de pastel
    pie_fig = px.pie(filtered_df, names='Country', values=selected_metric,
                    #  title=f'Distribución de {selected_metric} por país en el año seleccionado'
                    )

    # Gráfico de línea para el ratio
    ratio_line_fig = px.line(groupedYear, x='Year', y='ratio', color='Country',
                             labels={'ratio': f'Ratio {selected_metric}'},
                            #  title='Ratio Gasto País sobre la Media a lo largo de los años'
                             )
    
    # Agregar la línea horizontal en el valor 1 con Plotly
    ratio_line_fig.update_layout(
        shapes=[dict(type='line', yref='y', y0=1, y1=1, xref='x', x0=min(groupedYear['Year']),
                     x1=max(groupedYear['Year']), line=dict(color='black', dash='dash'))]
    )

    return line_fig, pie_fig, ratio_line_fig, titulo1, titulo2, titulo3

@app.callback(
    [Output('clicked_year', 'children'),
     Output('clicked_country', 'children'),
     Output('healthexp', 'children'),
     Output('spending', 'children'),
     Output('mean_world', 'children'),
     Output('world_healthexp', 'children'),
     Output('world_spending', 'children')],
    [Input('line-plot', 'clickData'),
     Input('metric-radio', 'value')],    
)

def update_line_plot(clickData,selected_metric):
    if clickData == None:
        return '2007','USA','Gasto: 7166.513 USD','Años de Vida: 78.1 y','Media Mundial','3987.78 USD','Años de Vida: 80.36 y'
    else:
        mean_world = 'Media Mundial'
        date = '{}'.format(clickData['points'][0]['x'])
        country = countries[clickData['points'][0]['curveNumber']]
        print(date)
        
        world_spending = 'Gasto: {} USD'.format(int(df1[(df1['Year'] == int(date))]['Spending_USD'].mean()*100)/100)
        world_healthexp = 'Años de Vida: {} y'.format(int(df2[(df2['Year'] == int(date))]['Life_Expectancy'].mean()*100)/100)

        
        if(selected_metric == 'Spending_USD'):
            spending = 'Gasto: {} USD'.format(clickData['points'][0]['y'])
            healthexp = 'Años de Vida: {} y'.format(df2[(df2['Year'] == int(date)) & (df2['Country'] == country)]['Life_Expectancy'].iloc[0])
        else:
            healthexp = 'Años de Vida: {} y'.format(clickData['points'][0]['y'])
            spending = 'Gasto: {} USD'.format(df1[(df1['Year'] == int(date)) & (df1['Country'] == country)]['Spending_USD'].iloc[0])
        return date,country,spending,healthexp,mean_world,world_spending,world_healthexp


if __name__ == '__main__':
    app.run_server(debug=True)