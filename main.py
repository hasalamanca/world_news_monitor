import sys
import os
import news_api as nws
import visualization as vis
from translate_to_eng import translate_headlines
from sentiment_module import analyze_sentiments
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

api_key = os.getenv("NEWS_API_KEY")

if __name__=="__main__":
    if len(sys.argv) < 2:
        print("Please provide an option: 'update' or 'visualize'")
        sys.exit(1)
    
    sources_traking_file_name = "sources_tracking.csv"
    headlines_repo_file_name = "headlines_repo.csv"

    news_api = nws.NewsAPI(api_key, headlines_repo_file_name, sources_traking_file_name)
    
    ## This is the master table to which we will add the metrics and filters we want so see more info on.
    headlines_repo = news_api.load_df_from_file(headlines_repo_file_name) # Load the data
    
    sources_list, sources_df = news_api.sources_to_download()

    if sys.argv[1] == 'update':
        # Update news titles and identify their source and country.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

        input("Before we start, please close all excel files and press enter to continue...")
        try:
            news_api.get_more_news()
        except Exception as e:
            print(f"Error raised: {e}")
            
        ## Function to translate text from any language to english
        headlines_repo = translate_headlines(headlines_repo)

        ## Sentiment analysis of the news  
        headlines_repo = analyze_sentiments(headlines_repo)
        

        # Optionally, save the results to a new CSV file
        file_path = os.path.join(os.getcwd(), headlines_repo_file_name)
        headlines_repo.to_csv(file_path, index=False)
        print(f"Translation and Sentiment Analysis completed. Results saved to {headlines_repo_file_name}.")

        ## Schedule the process to run periodically and use command line or equivalent

    elif sys.argv[1] == 'visualize':
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

        # Create choropleth maps
        st.set_page_config(layout="wide")
        st.title("World News Panel")

        tab1, tab2, tab3 = st.tabs(["Unique Sources", "Average Sentiment", "News Table"])

        with tab1:
            st.plotly_chart(vis.sources_per_country(headlines_repo), use_container_width=True)
        with tab2:
            st.plotly_chart(vis.sentiment_per_country(headlines_repo), use_container_width=True)
        with tab3:
            st.table(headlines_repo[["publishedAt","country", "source_id", "title_eng", "description_eng", "sentiment", "url"]].iloc[:100].sort_values(by="publishedAt", ascending=False))


##To Solve:

## Decide where and how we use command line
##Code is excecuting twice 
##Remove gibberish values
##black out empty data in the map



