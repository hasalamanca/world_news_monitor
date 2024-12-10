#pip install dash, plotly, pycountry
import pandas as pd
import plotly.express as px
import pycountry
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# Function to convert ISO-2 country codes to ISO-3
def iso2_to_iso3(iso2):
    try:
        return pycountry.countries.get(alpha_2=iso2.upper()).alpha_3
    except:
        return None

# Function to adjust country codes for visualization
def adjust_country_code_for_visualization(df):
    df['iso_3'] = df['country'].apply(iso2_to_iso3)
    df = df.dropna(subset=['iso_3'])
    return df

# Function to create a choropleth map for sources per country
def sources_per_country(df):
    country_counts = df.groupby('iso_3')['source_id'].nunique().reset_index()
    country_counts.columns = ['country', 'number_of_unique_sources']
    iso3_to_name = {country.alpha_3: country.name for country in pycountry.countries}
    country_counts['country_name'] = country_counts['country'].map(iso3_to_name)
    fig = px.choropleth(
        country_counts,
        locations='country',
        color='number_of_unique_sources',
        hover_name='country_name',
        color_continuous_scale=px.colors.sequential.Plasma,
        projection='natural earth',
        title='World News Panel - Number of Unique Sources'
    )
    return fig

# Function to create a choropleth map for sentiment per country
def sentiment_per_country(df):
    country_sentiment = df.groupby('iso_3')['sentiment'].mean().reset_index()
    country_sentiment.columns = ['country', 'average_sentiment']
    iso3_to_name = {country.alpha_3: country.name for country in pycountry.countries}
    country_sentiment['country_name'] = country_sentiment['country'].map(iso3_to_name)
    fig = px.choropleth(
        country_sentiment,
        locations='country',
        color='average_sentiment',
        hover_name='country_name',
        color_continuous_scale=px.colors.diverging.RdBu,
        projection='natural earth',
        title='World News Panel - Average Sentiment'
    )
    return fig

# Function to run the Dash app
def run_dashboard(df):
    df = adjust_country_code_for_visualization(df)
    
    # Initialize the Dash app
    app = dash.Dash(__name__)

    # Define the layout of the app
    app.layout = html.Div([
        html.H1(id='dashboard-title', children="World News Dashboard"),
        html.P(id='dashboard-description', children="This dashboard displays visualizations of world news data."),
        html.Button('Show Sources per Country', id='sources-button', n_clicks=0),
        html.Button('Show Sentiment per Country', id='sentiment-button', n_clicks=0),
        dcc.Graph(id='choropleth-map', figure=sources_per_country(df))
    ])

    # Callback to update the choropleth map
    @app.callback(
        Output('choropleth-map', 'figure'),
        [Input('sources-button', 'n_clicks'),
         Input('sentiment-button', 'n_clicks')]
    )
    def update_map(n_sources, n_sentiment):
        if n_sources == 0 and n_sentiment == 0:
            return dash.no_update
        elif n_sources > n_sentiment:
            return sources_per_country(df)
        else:
            return sentiment_per_country(df)

    # Run the app
    app.run_server(debug=True, use_reloader=False)




