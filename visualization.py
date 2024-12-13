import pandas as pd
import plotly.express as px
import pycountry

def iso2_to_iso3(iso2):
    """Convert ISO-2 country codes to ISO-3."""
    try:
        return pycountry.countries.get(alpha_2=iso2.upper()).alpha_3
    except:
        return None

def adjust_country_code_for_visualization(df):
    """Adjust country codes for visualization."""
    df['iso_3'] = df['country'].apply(iso2_to_iso3)
    return df.dropna(subset=['iso_3'])

def create_choropleth(df, value_column, agg_func, color_scale, title):
    """Create a choropleth map."""
    df = adjust_country_code_for_visualization(df)
    data = df.groupby('iso_3')[value_column].agg(agg_func).reset_index()
    data.columns = ['country', value_column]
    iso3_to_name = {country.alpha_3: country.name for country in pycountry.countries}
    data['country_name'] = data['country'].map(iso3_to_name)
    
    fig = px.choropleth(
        data,
        locations='country',
        color=value_column,
        hover_name='country_name',
        color_continuous_scale=color_scale,
        projection='natural earth',
        title=title,
    )
    fig.update_layout(
        autosize=True,
        width=None,
        height=600,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig

def sources_per_country(df):
    """Create a choropleth map for sources per country."""
    return create_choropleth(df, 'source_id', 'nunique', px.colors.sequential.YlGn, 'Number of Unique Sources')

def sentiment_per_country(df):
    """Create a choropleth map for sentiment per country."""
    return create_choropleth(df, 'sentiment', 'mean', px.colors.diverging.RdBu, 'Average Sentiment')