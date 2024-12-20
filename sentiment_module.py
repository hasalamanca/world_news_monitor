import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiments(df):
    print("Analyzing sentiments...")
    # Initialize the VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Check if 'title' and 'description' columns exist
    if 'title' not in df.columns or 'description' not in df.columns:
        raise ValueError("DataFrame must contain 'title' and 'description' columns.")

    # Fill missing values with empty strings to handle empty fields
    df['title_eng'] = df['title_eng'].fillna('')
    df['description_eng'] = df['description_eng'].fillna('')

    # Combine 'title' and 'description' into 'combined_text'
    df['combined_text'] = df['title_eng'].astype(str) + ' ' + df['description_eng'].astype(str)

    # Define a function to compute the sentiment score for a given text
    def get_sentiment(text):
        if text.strip() == '':
            return None  # Return None if the combined text is empty
        else:
            scores = analyzer.polarity_scores(text)
            return scores['compound']  # Use 'compound' score as the overall sentiment

    # Apply the sentiment function to the 'combined_text' column
    df['sentiment'] = df['combined_text'].apply(get_sentiment)

    # Optionally, drop the 'combined_text' column if it's no longer needed
    df.drop(columns=['combined_text'], inplace=True)
    return df
