#pip install googletrans==4.0.0-rc1

from googletrans import Translator
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

file_name="headlines_repo.csv"
# Ensure the file is loaded from the local directory
file_path = os.path.join(os.getcwd(), file_name)
df = pd.read_csv(file_path, encoding='utf-8')

print(f"DataFrame loaded from {file_path}")

print(df)

translator = Translator()

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
            continue
    if pd.isna(row['description_eng']) and row['language'] != 'en':
        try:
            translated = translator.translate(row['description'])
            df.at[index, 'description_eng'] = translated.text
        except Exception as e:
            print(f"Failed to translate description at index {index}: {e}")
            continue

print("finished translating, will save now")

print(df)
file_name="headlines_repo_translated.csv"
# Ensure the file is loaded from the local directory
file_path = os.path.join(os.getcwd(), file_name)

df.to_csv(file_path, index=False, encoding='utf-8')
print(f"Updated DataFrame saved to {file_path}")


#translated=translator.translate('안녕하세요.')

#print(translated.text)