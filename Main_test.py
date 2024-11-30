# sentiment_analysis_on_csv.py

import pandas as pd
from sentiment_module import analyze_sentiments

# Read the DataFrame from the CSV file
df = pd.read_csv('sample_data.csv')

# Apply sentiment analysis
df_result = analyze_sentiments(df)

# Display the DataFrame with sentiment scores
print(df_result)

# Optionally, save the results to a new CSV file
df_result.to_csv('sample_data_with_sentiment.csv', index=False)
print("Sentiment analysis completed. Results saved to 'sample_data_with_sentiment.csv'.")
