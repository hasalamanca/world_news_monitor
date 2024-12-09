#pip install vaderSentiment
#pip install googletrans==4.0.0-rc1
#pip install dash, plotly, pycountry

import os
import sentiment_module as sm
import news_api as nws
import visualization as vis
import translate_to_eng as tte

api_key = "0300f083ebd946b180af8a9bca9895c7"

## Update news titles and identify their source and country.
#This needs to run automatically every day to update the panel.
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

sources_traking_file_name = "sources_tracking.csv"
headlines_repo_file_name = "headlines_repo.csv"

input("Before we start, please close all excel files and press enter to continue...")

try:
    sources_list, sources_df = nws.sources_to_download(sources_traking_file_name, api_key)
    nws.get_more_news(api_key, sources_list, sources_df, headlines_repo_file_name, sources_traking_file_name)
except Exception as e:
    print(f"Error raised: {e}")
    
## This is the master table to which we will add the metrics and filters we want so see more info on.

headlines_repo =nws.load_df_from_file(headlines_repo_file_name) # Load the data

## Function to translate text from any language to english

headlines_repo=tte.translate_headlines(headlines_repo)

## Sentiment analysis of the news
  
headlines_repo = sm.analyze_sentiments(headlines_repo)
#print(headlines_repo)

# Optionally, save the results to a new CSV file
file_path = os.path.join(os.getcwd(), headlines_repo_file_name)
headlines_repo.to_csv(file_path, index=False)
print(f"Translation and Sentiment Analysis completed. Results saved to {headlines_repo_file_name}.")

## Schedule the process to run periodically and use command line or equivalent

#Tables I would like to visualize nicely on the dashboard that can sort and filter
print("1. List of sources per country")
print(sources_df[["name", "country"]].sort_values(by="name").drop_duplicates())

print("2. Average sentiment per country")
print("Top 5 positive sentiment countries")
print(headlines_repo[["country", "sentiment"]].groupby("country").mean().sort_values(by="sentiment").tail(5))
print("Top 5 negative sentiment countries")
print(headlines_repo[["country", "sentiment"]].groupby("country").mean().sort_values(by="sentiment").head(5))

print("3. Country, source, title_eng, description_eng, sentiment, url") #This table it would be ideal if it could be filtered by country and source.
print(headlines_repo[["publishedAt","country", "source_id", "title_eng", "description_eng", "sentiment", "url"]].sort_values(by="publishedAt", ascending=False))


## UI work, how to smartly add filter, buttons to search for keywords, consider time period average of the metrics at display, etc. Could be a google sheets.
print("Running the dashboard to visualize...")
vis.run_dashboard(headlines_repo)




##To Solve:

## Decide where and how we use command line
##Code is excecuting twice 
##Remove gibberish values
##black out empty data in the map



