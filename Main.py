import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

# Load dataset
df_fifa = pd.read_csv('players_22.csv')

# Load continents2.csv
df_continents = pd.read_csv('continents2.csv')

# Function to map country to region and alpha-3
def map_country_to_region(country):
    country_info = df_continents[df_continents['name'] == country]
    if not country_info.empty:
        return country_info['region'].values[0], country_info['alpha-3'].values[0]
    else:
        return 'Other', 'Other'  # Default values if country not found

# Add 'region' and 'alpha-3' columns to df_fifa
df_fifa[['region', 'alpha-3']] = df_fifa['nationality_name'].apply(lambda x: pd.Series(map_country_to_region(x)))

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# Define function to prioritize main position
def prioritize_position(player_positions):
    return player_positions.split(',')[0]  # Prioritize by the first position listed

# Map positions to general categories
def map_positions(player_positions):
    if player_positions in ['GK']:
        return 'Goalkeeper'
    elif player_positions in ['CB', 'RB', 'LB', 'RWB', 'LWB']:
        return 'Defender'
    elif player_positions in ['CM', 'CAM', 'CDM', 'RM', 'LM']:
        return 'Midfielder'
    elif player_positions in ['ST', 'RW', 'LW', 'CF']:
        return 'Forward'
    else:
        return 'Other'

# Define the layout of the Dash app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Football Players Data Visualization 2022", style={'text-align': 'center', 'color': '#ffffff'}), width=12)
    ], style={'background-color': '#111111', 'padding': '10px', 'border': '6px solid #ffffff'}),

    dbc.Row([
        dbc.Col([
            html.Label("Select Preferred Foot:", style={'color': '#ffffff','font-size':'12px'}),
            dcc.Dropdown(
                id='preferred-foot-dropdown',
                options=[
                    {'label': 'Left', 'value': 'Left'},
                    {'label': 'Right', 'value': 'Right'}
                ],
                value='Right',  # Default value
                style={'width': '100%', 'color': 'black', 'background-color': '#ffffff'}
            ),
        ], width=3, style={'margin-top': '20px', 'margin-bottom': '20px'})
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='scatter-plot'),
        ], width=8),
        dbc.Col([
            html.Div(id='player-info', style={'border': '5px solid white', 'padding': '10px', 'border-radius': '10px'}),
        ], width=4),
    ]),

    dbc.Row([
        dbc.Col([
            html.Label("Select Age Range:", style={'color': '#ffffff'}),
            dcc.RangeSlider(
                id='age-slider',
                min=df_fifa['age'].min(),
                max=df_fifa['age'].max(),
                value=[df_fifa['age'].min(), df_fifa['age'].max()],
                marks={str(age): str(age) for age in range(df_fifa['age'].min(), df_fifa['age'].max() + 1, 5)},
                step=None,
                included=True,
                pushable=1,
                allowCross=False,
                tooltip={'placement': 'bottom'},
                className='range-slider'
            ),
        ], width=6)
    ], style={'margin': 'auto', 'padding': '20px'}),

    dbc.Row([
        dbc.Col([
            html.Label("Select Region:", style={'color': '#ffffff'}),
            dcc.Dropdown(
                id='region-dropdown',
                options=[
                    {'label': 'All', 'value': 'All'}
                ] + [{'label': region, 'value': region} for region in df_fifa['region'].unique()],
                value='All',  # Default value
                style={'width': '100%', 'color': 'black', 'background-color': '#ffffff'}
            )
        ], width=2, style={'padding': '20px'}),
        dbc.Col([
            dcc.Graph(id='geo-map'),
        html.Div(id='top-players') ], width=9)
    ], style={'background-color': '#111111', 'padding': '20px', 'border': '2px solid #ffffff'})
], fluid=True, style={'background-color': '#111111', 'padding': '20px'})

# Callback to update scatter plot based on dropdown and slider selection
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('preferred-foot-dropdown', 'value'),
     Input('age-slider', 'value')]
)
def update_scatter_plot(preferred_foot, age_range):
    filtered_df = df_fifa[(df_fifa['preferred_foot'] == preferred_foot) & 
                          (df_fifa['age'] >= age_range[0]) & 
                          (df_fifa['age'] <= age_range[1])]
    
    # Apply function to prioritize main position
    filtered_df['main_position'] = filtered_df['player_positions'].apply(prioritize_position)
    
    # Map positions to general categories
    filtered_df['general_position'] = filtered_df['main_position'].apply(map_positions)
    
    fig = px.scatter(filtered_df, x='age', y='overall', color='general_position', 
                     hover_name='short_name',
                     title=f'Scatter Plot of Overall Rating vs Age for {preferred_foot} Footed Players',
                     labels={'age': 'Age', 'overall': 'Overall', 'general_position': 'General Position'},
                     template='plotly_dark')
    
    total_players = len(filtered_df)
    fig.update_layout(
        annotations=[
            dict(
                x=0.5,
                y=-0.1,
                xref='paper',
                yref='paper',
                text=f'Total Players: {total_players}',
                showarrow=False,
                font=dict(
                    size=12,
                    color='white'
                ),
                bgcolor='rgba(0, 0, 0, 0.5)'
            )
        ]
    )
    
    return fig

# Callback to update choropleth map based on dropdown selection
@app.callback(
    Output('geo-map', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_choropleth(region):
    if region == 'All':
        filtered_df = df_fifa.copy()
    else:
        filtered_df = df_fifa[df_fifa['region'] == region]

    country_distribution = filtered_df['nationality_name'].value_counts().reset_index()
    country_distribution.columns = ['country', 'count']
    
    fig2 = px.choropleth(country_distribution, locations='country', locationmode='country names', 
                         color='count', 
                         title=f'Distribution of Players by Country in {region}',
                         labels={'country': 'Country', 'count': 'Player'},
                         template='plotly_dark', color_continuous_scale=px.colors.sequential.Inferno)
    
    return fig2

# Callback to display player info when scatter plot is clicked
@app.callback(
    Output('player-info', 'children'),
    [Input('scatter-plot', 'clickData')]
)
def display_player_info(clickData):
    if clickData is not None:
        player_name = clickData['points'][0]['hovertext']
        player_info = df_fifa[df_fifa['short_name'] == player_name].iloc[0]
        
        player_name = player_info['short_name']
        age = player_info['age']
        overall = player_info['overall']
        alpha3_code = player_info['alpha-3']
        photo_url = player_info['player_face_url']  
        club_url = player_info['club_logo_url']
        nation_logo_url = player_info['nation_flag_url']

         # Create HTML elements to display player info including the photo
        player_details = html.Div([
            html.Div([
                html.Img(src=nation_logo_url, style={'width': '50px', 'height': 'auto', 'display': 'block', 'margin': 'auto'}),
                html.P(alpha3_code, style={'text-align': 'center', 'margin': '5px 0'})
            ], style={'display': 'inline-block', 'width': '50px', 'float': 'left', 'margin-right': '10px'}),
            html.Img(src=club_url, style={'width': '50px', 'height': 'auto', 'float': 'right', 'margin-right': '10px'}),
            html.Img(src=photo_url, style={'width': '200px', 'height': 'auto', 'display': 'block', 'margin': 'auto'}),
            html.H4(f'{player_name}', style={'text-align': 'center', 'margin-bottom': '5px'}),
            html.P(f'Overall: {overall}', style={'text-align': 'center', 'margin': '5px 0'})
        ])
        
        return player_details
    
    return html.Div('Click on a point in the scatter plot to see player details.')

# Callback to update top players as a chart based on geo-map click
@app.callback(
    Output('top-players', 'children'),
    [Input('geo-map', 'clickData')]
)
def display_top_players(clickData):
    if clickData is not None:
        selected_country = clickData['points'][0]['location']
        filtered_df = df_fifa[df_fifa['nationality_name'] == selected_country]
        
        if not filtered_df.empty:
            top_players = filtered_df.nlargest(10, 'value_eur')
            
            # Create bar chart for top players
            fig = px.bar(top_players, x='short_name', y='value_eur', color='value_eur',
                         title=f"Top 10 Players from {selected_country} by Value (in million euros)",
                         labels={'short_name': 'Player Name', 'value_eur': 'Value (million euros)'},
                         template='plotly_dark')
            
            fig.update_layout(xaxis={'categoryorder': 'total descending'})
            
            return dcc.Graph(figure=fig)
        else:
            return html.Div(f"No player data available for {selected_country}.")
    
    return html.Div("Click on a country in the geo-map to see top players.")


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
