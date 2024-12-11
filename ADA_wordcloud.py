import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import re
import string

# Make sure to download the stopwords list if not already done
# import nltk
# nltk.download('stopwords')

def generate_wordcloud(file_path):
    # Load the dataset
    df = pd.read_excel(file_path)

    # Parse 'publishedAt' column to datetime and handle missing values
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce', utc=True)
    df = df.dropna(subset=['publishedAt'])

    # Convert datetime to date for simplicity
    df['publishedAt'] = df['publishedAt'].dt.date

    # Filter data for the last month
    latest_date = max(df['publishedAt'])
    one_month_ago = latest_date.replace(month=latest_date.month - 1 if latest_date.month > 1 else 12)
    last_month_data = df[df['publishedAt'] >= one_month_ago]

    # Combine all text data from the 'title_eng' and 'description_eng' columns for the last month
    combined_text = ' '.join(last_month_data['title_eng'].fillna('').str.lower() + ' ' + last_month_data['description_eng'].fillna('').str.lower())

    # Define stopwords (customize or extend as needed)
    custom_stopwords = set(stopwords.words('english'))
    custom_stopwords.update(["news", "comprehensive", "coverage", "know", "x000d","world", "uptodate", "google", "date", "aggregated", "sources"])

    # Normalize text: remove punctuation and extra spaces
    normalized_text = re.sub(f"[{string.punctuation}]", "", combined_text)
    normalized_text = re.sub(r"\s+", " ", normalized_text).strip()

    # Remove stopwords
    filtered_text = ' '.join([word for word in normalized_text.split() if word not in custom_stopwords])

    # Generate a word cloud
    wordcloud = WordCloud(width=800, height=400, max_words=50, background_color='white').generate(filtered_text)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Top 50 Keywords from the Last Month', fontsize=16)
    plt.show()

# Usage Example
file_path = r"C:\Users\horac\OneDrive\Escritorio\headlines_repo.xlsx"
generate_wordcloud(file_path)
