import sys
import os
import news_api as nws
import visualization as vis
from translate_to_eng import translate_headlines
from sentiment_module import analyze_sentiments
from dotenv import load_dotenv
import streamlit as st
from EDA_wordcloud import generate_wordcloud
from EDA_sentiment_clusters import process_dataset_with_time_features
import warnings

warnings.filterwarnings("ignore")

load_dotenv()

api_key = os.getenv("NEWS_API_KEY")

if __name__=="__main__":
    if len(sys.argv) < 2:
        print("Please provide an option: 'update' or 'visualize'")
        sys.exit(1)
    
    sources_tracking_file_name = "sources_tracking.csv"
    headlines_repo_file_name = "headlines_repo.csv"

    news_api = nws.NewsAPI(api_key, headlines_repo_file_name, sources_tracking_file_name)
    
    ## This is the master table to which we will add the metrics and filters we want so see more info on.
    headlines_repo = news_api.load_df_from_file(headlines_repo_file_name) # Load the data
    if sys.argv[1] == 'update':
        sources_list, sources_df = news_api.sources_to_download(update=True)
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
        sources_list, sources_df = news_api.sources_to_download()
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
        st.title("World News Monitor")

        tab1, tab2, tab3 = st.tabs(["Home", "Sentiment", "News Panel"])

        with tab1:
            st.markdown(
"""Welcome to the world news monitor, the world wide panel where you can access more than one hundred outlets translated to english and evaluated according to their sentiment.

You want to know what is going on, visit the World News Monitor, soon to be WNM.es"""
                )
            col1, col2 = st.columns([2, 1])
    
            with col1:
                st.plotly_chart(vis.sources_per_country(headlines_repo), use_container_width=True)
            
            with col2:
                country_list = headlines_repo['country'].unique()
                selected_country = st.selectbox("Select a country to filter sources:", country_list)
                filtered_sources = headlines_repo[headlines_repo['country'] == selected_country][['source_name']].drop_duplicates()
                st.dataframe(filtered_sources)
            st.markdown("And we bring your favorite, our world trends:")
            col1, col2, col3 = st.columns([2,4,2])
            with col1:
                st.write("")
            with col2:
                st.image(generate_wordcloud(headlines_repo).to_image())
            with col3:
                st.write("")
        with tab2:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("### Top 5 Positive Sentiment Countries")
                top_5_positive = headlines_repo.groupby('country')['sentiment'].mean().sort_values(ascending=False).head(5).reset_index()
                st.dataframe(top_5_positive)
            with col2:
                st.markdown("### Top 5 Negative Sentiment Countries")
                bottom_5_negative = headlines_repo.groupby('country')['sentiment'].mean().sort_values(ascending=True).head(5).reset_index()
                st.dataframe(bottom_5_negative)
            st.markdown("News sentiment gives a powerful view of what people are being fed by the media. This can alter a nations mood and reflect different opinions versus the same topic. For example the US elections.")
            st.plotly_chart(vis.sentiment_per_country(headlines_repo), use_container_width=True)
            st.markdown("If we analyze how the news sentiment relates between different countries we can identify relevant clusters:")
            st.plotly_chart(process_dataset_with_time_features(headlines_repo), use_container_width=True)
        with tab3:
            st.markdown("""
If only could see all news outlets in one place... wait you can, look below!

You can filter per country, news outlet, sort by sentiment and date."""
                        )
            country_list = headlines_repo['country'].unique()
            source_list = headlines_repo['source_id'].unique()
            
            selected_country = st.selectbox("Select a country to filter news:", ['All'] + list(country_list))
            selected_source = st.selectbox("Select a news source to filter news:", ['All'] + list(source_list))
            
            filtered_news = headlines_repo.dropna(subset=['publishedAt'])
            
            if selected_country != 'All':
                filtered_news = filtered_news[filtered_news['country'] == selected_country]
            
            if selected_source != 'All':
                filtered_news = filtered_news[filtered_news['source_id'] == selected_source]
            
            st.dataframe(filtered_news[["publishedAt","country", "source_id", "title_eng", "description_eng", "sentiment", "url"]].sort_values(by="publishedAt", ascending=False))

