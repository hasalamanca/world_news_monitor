
import requests
import pandas as pd
import os  #For saving local copies of the files
from datetime import datetime #Publishing time to an easier to handle date time


def fetch_news_sources(api_key):

    url = f"https://newsapi.org/v2/top-headlines/sources?apiKey={api_key}"

    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        sources = data.get("sources", [])
        
        # Create and return a DataFrame
        return pd.DataFrame(sources)
    else:
        # Handle errors
        raise Exception(f"Error fetching data: {response.status_code}, {response.text}")


def fetch_news_headlines(api_key, source_id):

    url = f"https://newsapi.org/v2/top-headlines?sources={source_id}&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        headlines = data.get("articles", [])  # Fetch headlines from the "articles" key
        
        # Convert to DataFrame
        headlines_df = pd.DataFrame(headlines)
        
        # Replace 'source' with its 'id'
        headlines_df['source'] = source_id
        
        # Drop unnecessary columns
        headlines_df.drop(columns=['urlToImage', 'content'], inplace=True, errors='ignore')
        
        # Format 'publishedAt' to a readable datetime format
        #if 'publishedAt' in headlines_df.columns:
        #    headlines_df['publishedAt'] = pd.to_datetime(headlines_df['publishedAt']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        return headlines_df
    else:
        raise Exception(f"Error fetching headlines for {source_id}: {response.status_code}, {response.text}")


def merge_main_news_table(sources_df, headlines_df):

    # Rename 'id' in sources_df to 'source' for alignment with headlines_df
    sources_df = sources_df.rename(columns={"id": "source"})
    sources_df.drop(columns=['description', 'url'], inplace=True, errors='ignore')

    # Perform the join
    # Inner to secure the most integrity on the data included
    combined_df = pd.merge(headlines_df, sources_df, on=["source", "name"], how="inner")

    # Rename columns
    combined_df = combined_df.rename(columns={"source": "source_id", "name": "source_name"})
    
    # Reorder the columns
    column_order = [
        "publishedAt",
        "source_id",
        "source_name",
        'category',
        "language",
        "country",
        "author",
        "title",
        "description",
        "url"
    ]
    combined_df = combined_df[column_order]
    
    return combined_df



def get_news_consolidates(api_key, sources_tracking, headlines_depot):
    sources_df = fetch_news_sources(api_key)
    headlines_df = pd.DataFrame()
    for source in sources_df["id"]:    
        if headlines_df.empty:
            headlines_df = fetch_news_headlines(api_key, source)
        else:
            headlines_df = pd.concat([headlines_df, fetch_news_headlines(api_key, source)], ignore_index=True)
    return merge_main_news_table(sources_df, headlines_df)








################################################################

def save_df_to_file(df, file_name):

    # Ensure the file is saved in the local directory
    file_path = os.path.join(os.getcwd(), file_name)
    df.to_csv(file_path, index=False)
    print(f"DataFrame saved to {file_path}")

def load_df_from_file(file_name):

    # Ensure the file is loaded from the local directory
    file_path = os.path.join(os.getcwd(), file_name)
    df = pd.read_csv(file_path)
    print(f"DataFrame loaded from {file_path}")
    return df

################################################################

api_key = "0300f083ebd946b180af8a9bca9895c7"

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


##I get the data and save the most updated version.
#df = fetch_news_sources(api_key)
#save_df_to_file(df, "news_sources.csv")

#df = fetch_news_headlines(api_key, "abc-news")
#save_df_to_file(df, "news_titles.csv")

#I retrieve saved data
#df_news_sources= load_df_from_file("news_sources.csv")
#df_news_titles= load_df_from_file("news_titles.csv")


save_df_to_file(get_news_consolidates(api_key), "full_db_sample.csv")



"""

from newsapi import NewsApiClient
import pandas as pd
import pycountry



def summary_sources():
    
    return

#Credentials

## Using the API to get the data

newsapi = NewsApiClient(api_key='0300f083ebd946b180af8a9bca9895c7')

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                          sources='bbc-news,the-verge',
                                          category='business',
                                          language='en',
                                          country='us')

print(top_headlines)

                                          

# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2017-12-01',
                                      to='2017-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)
"""


"""
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


"""