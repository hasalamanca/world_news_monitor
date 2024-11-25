

##Setting up the imports

# API Key 0300f083ebd946b180af8a9bca9895c7
#pip install newsapi-python


from newsapi import NewsApiClient
import pandas as pd
import plotly.express as px
import pycountry



## Using the API to get the data

newsapi = NewsApiClient(api_key='0300f083ebd946b180af8a9bca9895c7')

""" # /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                          sources='bbc-news,the-verge',
                                          category='business',
                                          language='en',
                                          country='us')

# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2017-12-01',
                                      to='2017-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2) """

# /v2/top-headlines/sources
input_sources = newsapi.get_sources()


## Process the data for a readable output and set the master table.

sources = input_sources['sources']

# Create a list to hold the table data
table_data = []

# Iterate over each source and extract 'country', 'language', 'name'
for source in sources:
    country = source.get('country', '')
    language = source.get('language', '')
    name = source.get('name', '')
    table_data.append({'Country': country, 'Language': language, 'Name': name})

# Using pandas to work on df

df = pd.DataFrame(table_data)

# Count the number of sources per country
country_counts = df['Country'].value_counts().reset_index()
country_counts.columns = ['Country', 'Number of Sources']

# Display the summary table
print("\nSummary Table of Sources per Country:")
print(country_counts)

#This is the master table to which we will add the metrics and filters we want so see more info on.

## Function to translate text from any language to english

## Get news titles and identify their source, country and category

## Find sentiment analysis tools we can use to create metrics to measure: Excitement, Alarm, Unemotional, Fear, etc.

## Schedule the process to run periodically, add a time stamp and identify the way the history of the analysis can be stored.

## UI work, how to smartly add filter, buttons to search for keywords, consider time period average of the metrics at display, etc. Could be a google sheets.

## Create a choropleth map

##Ensure command line execution

##*classes and modules

# Convert country codes to ISO-3 (3-letter country codes)
def iso2_to_iso3(iso2):
    try:
        return pycountry.countries.get(alpha_2=iso2.upper()).alpha_3
    except:
        return None

# Apply the conversion to the 'Country' column
df['ISO-3'] = df['Country'].apply(iso2_to_iso3)

# Remove entries with invalid or missing ISO-3 codes
df = df.dropna(subset=['ISO-3'])

# Create a summary table of sources per country
country_counts = df['ISO-3'].value_counts().reset_index()
country_counts.columns = ['Country', 'Number of Sources']

# Sentiment analysis, create values that add importance


#

# Adding country names for better readability
iso3_to_name = {country.alpha_3: country.name for country in pycountry.countries}
country_counts['Country Name'] = country_counts['Country'].map(iso3_to_name)

# Create the choropleth map using Plotly Express
fig = px.choropleth(
    country_counts,
    locations='Country',
    color='Number of Sources',
    hover_name='Country Name',
    color_continuous_scale=px.colors.sequential.Plasma,
    projection='natural earth',
    title='World News Panel'
)

# Display the map
fig.show()

