import requests
import pandas as pd
import os
from datetime import datetime

class NewsAPI:
    def __init__(self, api_key, headlines_repo, sources_tracking_file_name):
        self.api_key = api_key
        self.headlines_repo = headlines_repo
        self.sources_tracking_file_name = sources_tracking_file_name

    def save_df_to_file(self, df, file_name):
        print("Saving DataFrame to file...")
        file_path = os.path.join(os.getcwd(), file_name)
        if os.path.exists(file_path):
            df.to_csv(file_path, mode="a", index=False, header=False, encoding="utf-8")
        else:
            df.to_csv(file_path, index=False, encoding="utf-8")
        print(f"DataFrame saved to {file_path}")

    def load_df_from_file(self, file_name):
        file_path = os.path.join(os.getcwd(), file_name)
        print(f"Loading DataFrame from {file_path}")
        df = pd.read_csv(file_path, encoding='utf-8')
        print("DataFrame loaded successfully.")
        return df

    def append_row_to_csv(self, file_name, new_row):
        new_row_df = pd.DataFrame([new_row])
        new_row_df.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8')

    def fetch_news_sources(self, update=False):
        if update:
            print("Fetching news sources...")
            url = f"https://newsapi.org/v2/top-headlines/sources?apiKey={self.api_key}"
            try:
                response = requests.get(url)
            except:
                raise Exception("Error fetching sources")
            if response.status_code == 200:
                data = response.json()
                sources = data.get("sources", [])
                sources = pd.DataFrame(sources)
                print("Sources retrieved")
                return sources
            else:
                raise Exception(f"Error fetching data: {response.status_code}, {response.text}")

    def fetch_news_headlines(self, source_id):
        print(f"Fetching headlines for {source_id}...")
        url = f"https://newsapi.org/v2/top-headlines?sources={source_id}&sortBy=publishedAt&apiKey={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            headlines = data.get("articles", [])
            headlines_df = pd.DataFrame(headlines)
            headlines_df['source'] = source_id
            headlines_df.drop(columns=['urlToImage', 'content'], inplace=True, errors='ignore')
            print("Headlines retrieved")
            return headlines_df
        else:
            raise Exception(f"Error fetching headlines for {source_id}: {response.status_code}, {response.text}")

    def format_main_news_table(self, sources_df, headlines_df):
        print("format_main_news_table: Merging sources and headlines...")
        sources_df = sources_df.rename(columns={"id": "source"})
        sources_df.drop(columns=['description', 'url'], inplace=True, errors='ignore')
        combined_df = pd.merge(headlines_df, sources_df, on=["source"], how="inner")
        combined_df = combined_df.rename(columns={"source": "source_id", "name": "source_name"})
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
        combined_df['sentiment'] = None
        return combined_df

    def sources_to_download(self, update=False):
        try:
            sources_tracking = pd.read_csv(self.sources_tracking_file_name)
        except:
            print("No tracking file found. Creating a new one.")
            sources_tracking = pd.DataFrame(columns=['id', 'timestamp'])
        sources_tracking.columns = ['id', 'count']
        sources_tracking = sources_tracking['id'].value_counts().reset_index()
        try:
            if update:
                sources_df_original = self.fetch_news_sources(update=True)
            else:
                sources_df_original = self.load_df_from_file("sources_repo.csv")
        except:
            raise Exception("Error fetching sources.\nThe free service allows 100 requests per day.\nPlease try to update later.")
        sources_df = sources_df_original['id']
        sources_tracking = pd.merge(sources_tracking, sources_df, on='id', how='outer')
        sources_tracking['count'] = sources_tracking['count'].fillna(0)
        sources_tracking.sort_values(by='count', inplace=True, ascending=True, ignore_index=True)
        prioritized_sources_list = sources_tracking['id'].to_list()
        self.save_df_to_file(sources_df_original, "sources_repo.csv")
        return prioritized_sources_list, sources_df_original

    def get_more_news(self, number_of_sources=10):
        print("Getting more news...")
        sources_list, sources_df = self.sources_to_download()
        print("Sources list: ", sources_list)
        print("headlines_repo: ", self.headlines_repo)
        headlines_df = pd.DataFrame()
        for source_id in sources_list[:number_of_sources]:
            try:
                new_headlines = self.fetch_news_headlines(source_id)
                new_row = {'id': source_id, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                self.append_row_to_csv(self.sources_tracking_file_name, new_row)
                if headlines_df.empty:
                    headlines_df = new_headlines
                else:
                    headlines_df = pd.concat([headlines_df, new_headlines], ignore_index=True)
            except Exception as e:
                print(f"Error processing source {source_id}: {e}")
                break
        try:
            merged_df = self.format_main_news_table(sources_df, headlines_df)
        except Exception as e:
            print(f"Error merging sources and headlines: {e}")
            return
        if os.path.exists(self.headlines_repo):
            existing_repo = pd.read_csv(self.headlines_repo)
        else:
            existing_repo = pd.DataFrame()
        final_df = pd.concat([existing_repo, merged_df], ignore_index=True)
        final_df.drop_duplicates(subset=["publishedAt", "title"], keep="first", inplace=True)
        try:
            self.save_df_to_file(final_df, self.headlines_repo)
        except Exception as e:
            print(f"Error saving consolidated news: {e}")
            self.save_df_to_file(final_df, self.headlines_repo + "backup")
            return print("Consolidated news saved on backup file.")
        print("Consolidated news saved successfully.")
        return merged_df