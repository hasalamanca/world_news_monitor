
##Setting up the imports
#https://newsapi.org/docs/get-started
#pip install newsapi-python

import requests
import pandas as pd
import os  #For saving local copies of the files
from datetime import datetime #Publishing time to an easier to handle date time

def save_df_to_file(df, file_name):
    print("Saving DataFrame to file...")
    #print(df.columns)
    
    # Ensure the file is saved in the local directory
    file_path = os.path.join(os.getcwd(), file_name)
    
    # Check if the file already exists
    if os.path.exists(file_path):
        # Append to the file without writing the header
        df.to_csv(file_path, mode="a", index=False, header=False, encoding="utf-8") ##, sep=';')
    else:
        # Write the file with the header if it doesn't exist
        df.to_csv(file_path, index=False, encoding="utf-8") ##, sep=';')
    
    print(f"DataFrame saved to {file_path}")

def load_df_from_file(file_name):

    # Ensure the file is loaded from the local directory
    file_path = os.path.join(os.getcwd(), file_name)
    print(f"Loading DataFrame from {file_path}")

    df = pd.read_csv(file_path, encoding='utf-8') ## , sep=';')

    print("DataFrame loaded successfully.")
    return df

def append_row_to_csv(file_name, new_row):
    # Create a DataFrame with the new row
    new_row_df = pd.DataFrame([new_row])
    
    # Append the new row to the CSV file
    new_row_df.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8') #, sep=';')

def fetch_news_sources(api_key):
    
    print("Fetching news sources...")
    
    url = f"https://newsapi.org/v2/top-headlines/sources?apiKey={api_key}"

    #print(url) 

    # Make the GET request
    try:
        response = requests.get(url)
    except:
        raise Exception("Error fetching sources")

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        sources = data.get("sources", [])
        
        # Create and return a DataFrame
        
        sources = pd.DataFrame(sources)
        #print(sources)
        print("Sources retreived")
        return sources
    
    else:
        # Handle errors
        raise Exception(f"Error fetching data: {response.status_code}, {response.text}")

def fetch_news_headlines(api_key, source_id):
    print(f"Fetching headlines for {source_id}...")

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
        
        ##Disabled due to a suspicion that not all sources have same date format
        # Format 'publishedAt' to a readable datetime format
        #if 'publishedAt' in headlines_df.columns:
        #    headlines_df['publishedAt'] = pd.to_datetime(headlines_df['publishedAt']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        print("Headlines retreived")

        return headlines_df
    else:
        raise Exception(f"Error fetching headlines for {source_id}: {response.status_code}, {response.text}")

def format_main_news_table(sources_df, headlines_df):
    #Function to merge sources and headlines and format like the previous table for an append

    print("format_main_news_table: Merging sources and headlines...")

    # Rename 'id' in sources_df to 'source' for coherence with headlines_df
    sources_df = sources_df.rename(columns={"id": "source"})
    sources_df.drop(columns=['description', 'url'], inplace=True, errors='ignore')

    # Perform the join, inner to secure the most integrity on the data included
    combined_df = pd.merge(headlines_df, sources_df, on=["source"], how="inner")

    # Rename columns
    combined_df = combined_df.rename(columns={"source": "source_id", "name": "source_name"})

    #print("Combined df columns (pre order): ", combined_df.columns)

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

    combined_df['title_eng'] = None
    combined_df['description_eng'] = None
    combined_df['description_eng'] = None
    combined_df['sentiment'] = None

    #print("Final combined df columns: ", combined_df.columns)
    
    return combined_df

def sources_to_download(sources_tracking_file_name, api_key):
    
    try:
        sources_tracking = pd.read_csv(sources_tracking_file_name)
    except:
        print("No tracking file found. Creating a new one.")
        sources_tracking = pd.DataFrame(columns=['id', 'timestamp'])
    #print("Sources tracking: ", sources_tracking) ##Debugging
    sources_tracking.columns = ['id', 'count']
    #print("Sources tracking: ", sources_tracking) ##Debugging
    sources_tracking = sources_tracking['id'].value_counts().reset_index()

    try:
        sources_df_original = fetch_news_sources(api_key)
    except:
        raise Exception("Error fetching sources.\nThe free service allows 100 requests per day.\nPlease try to update later.")


    sources_df = sources_df_original['id']
                            
    sources_tracking = pd.merge(sources_tracking, sources_df, on='id', how='outer')
    sources_tracking['count'] = sources_tracking['count'].fillna(0)
    sources_tracking.sort_values(by='count', inplace=True, ascending=True, ignore_index=True)

    prioritized_sources_list= sources_tracking['id'].to_list()

    return prioritized_sources_list, sources_df_original

def get_more_news(api_key: str, sources_list: list, sources_df: pd.DataFrame, headlines_repo: str, sources_traking_file_name: str ):
    
    print("Getting more news...")
    print("Sources list: ", sources_list)
    print("headlines_repo: ", headlines_repo)

    headlines_df = pd.DataFrame()
    
    # Iterate over each row in sources_df
    for source_id in sources_list[:2]:  
        try:
            # Fetch headlines for the current source
            new_headlines = fetch_news_headlines(api_key, source_id)
            # Append register to source update tracking csv
            new_row = {'id': source_id, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            append_row_to_csv(sources_traking_file_name, new_row)

            # Append new headlines to the headlines_df
            if headlines_df.empty:
                headlines_df = new_headlines
            else:
                headlines_df = pd.concat([headlines_df, new_headlines], ignore_index=True)

        except Exception as e:
            print(f"Error processing source {source_id}: {e}")
            break #Stop the loop if an error is found

    # Merge sources and headlines
    # Inner merge to only add the fetched sources
    try:
        merged_df = format_main_news_table(sources_df, headlines_df) 
    except Exception as e:
        print(f"Error merging sources and headlines: {e}")
        return

    # Load existing headlines_repo
    if os.path.exists(headlines_repo):
        existing_repo = pd.read_csv(headlines_repo)
    else:
        existing_repo = pd.DataFrame()

    # Append results to existing_repo
    final_df = pd.concat([existing_repo, merged_df], ignore_index=True)

    # Remove duplicates based on 'publishedAt' and 'title'
    final_df.drop_duplicates(subset=["publishedAt", "title"], keep="first", inplace=True)

    # Save the final consolidated DataFrame to the CSV file
    try:
        save_df_to_file(final_df, headlines_repo)
    except Exception as e:
        print(f"Error saving consolidated news: {e}")
        save_df_to_file(final_df, headlines_repo + "backup")
        return print("Consolidated news saved on backup file.")

    print("Consolidated news saved successfully.")
    return merged_df


################################################################


#api_key = "0300f083ebd946b180af8a9bca9895c7"
#sources_traking_file_name = "sources_tracking.csv"
#headlines_repo_file_name = "headlines_repo.csv"
#sources_list, sources_df = sources_to_download(sources_traking_file_name, api_key)
#get_more_news(api_key, sources_list, sources_df, headlines_repo_file_name, sources_traking_file_name)

