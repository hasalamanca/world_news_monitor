#pip install googletrans==4.0.0-rc1

from googletrans import Translator
import pandas as pd
import os

def translate_headlines(df):


    # Ensure the file is loaded from the local directory
    #df = pd.read_csv(file_path, encoding='utf-8')
    #print(f"DataFrame loaded from {file_path}")

    print("Translating headlines...")
    translator = Translator()
    index_to_delete = []

    for index, row in df.iterrows():
        if pd.isna(row['title_eng']) and row['language'] == 'en':
            df.at[index, 'title_eng'] = df.at[index, 'title']
        if pd.isna(row['description_eng']) and row['language'] == 'en':
            df.at[index, 'description_eng'] = df.at[index, 'description']
        if pd.isna(row['title_eng']) and row['language'] != 'en':
            try:
                translated = translator.translate(row['title'])
                df.at[index, 'title_eng'] = translated.text
            except Exception as e:
                print(f"Failed to translate title at index {index}: {e}")
                index_to_delete.append(index)
                continue
        if pd.isna(row['description_eng']) and row['language'] != 'en':
            try:
                translated = translator.translate(row['description'])
                df.at[index, 'description_eng'] = translated.text
            except Exception as e:
                print(f"Failed to translate description at index {index}: {e}")
                continue
        if isinstance(row['title'], str) and (row['title'].startswith("https://") or row['title'] == "[Removed]") or pd.isna(row['title']):
            index_to_delete.append(index)

    # Drop rows with failed title translations
    df.drop(index_to_delete, inplace=True)
    print(f"Deleted {len(index_to_delete)} rows with non-news text (blanks, urls, etc.)")

    print("Finished translating")

    print(df)
    
    # Ensure the file is saved to the local directory
    #file_name="headlines_repo.csv"
    #script_dir = os.path.dirname(os.path.abspath(__file__))
    #os.chdir(script_dir)
    #file_path = os.path.join(os.getcwd(), file_name)
    #df.to_csv(file_path, index=False, encoding='utf-8')
    #print(f"Updated Translated DataFrame saved to {file_path}")

    return df


#print(translate_headlines())
