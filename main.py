#pip install vaderSentiment
#pip install googletrans==4.0.0-rc1
#pip install dash, plotly, pycountry

import os
from sentiment_module import analyze_sentiments
from news_api import * #import functions from news_api
from visualization import run_dashboard

api_key = "0300f083ebd946b180af8a9bca9895c7"

## Update news titles and identify their source and country.
#This needs to run automatically every day to update the panel.
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

sources_traking_file_name = "sources_tracking.csv"
headlines_repo_file_name = "headlines_repo.csv"
headlines_repo_sentiment_file_name = "headlines_repo_sentiment.csv"

input("Before we start, please close all excel files and press enter to continue...")

try:
    sources_list, sources_df = sources_to_download(sources_traking_file_name, api_key)
    print("Sources retreived")
    get_more_news(api_key, sources_list, sources_df, headlines_repo_file_name, sources_traking_file_name)
except Exception as e:
    print(f"Error raised: {e}")
    

## This is the master table to which we will add the metrics and filters we want so see more info on.
print("Retrieving data for analysis...")
headlines_repo =load_df_from_file(headlines_repo_file_name) #This function comes from news api in case later we decide to change the origin of the news db


## Function to translate text from any language to english


## Sentiment analysis tool
# Display the DataFrame with sentiment scores
headlines_repo = analyze_sentiments(headlines_repo)
print(headlines_repo)

# Optionally, save the results to a new CSV file
file_path = os.path.join(os.getcwd(), headlines_repo_sentiment_file_name)
headlines_repo.to_csv(file_path, index=False)
print("Sentiment analysis completed. Results saved to 'headlines_repo_sentiment.csv'.")

## Schedule the process to run periodically and use command line or equivalent

## UI work, how to smartly add filter, buttons to search for keywords, consider time period average of the metrics at display, etc. Could be a google sheets.

run_dashboard(headlines_repo)


## Create a choropleth map

#Prepare visualization
# Load the data
# Set the working directory to the script's directory




##To Solve:
##Sentiment must read from title and description in english
##Sentiment must only update empty rows
## Decide where or how we use command line
##Code is excecuting twice
##Remove gibberish
##black out empty data in the map



