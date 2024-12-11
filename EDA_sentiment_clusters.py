import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px


def load_and_clean_data(df):
    # Parse 'publishedAt' column to datetime and extract only the date
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce', utc=True).dt.date
    return df

def calculate_country_sentiment(df):
    country_sentiment = df.groupby('country')['sentiment'].mean().reset_index()
    country_sentiment.columns = ['country', 'avg_sentiment']

    return country_sentiment

def calculate_time_based_sentiment(df):
    df['month'] = pd.to_datetime(df['publishedAt']).dt.to_period('M')
    time_sentiment = df.groupby(['country', 'month'])['sentiment'].mean().reset_index()
    time_sentiment.columns = ['country', 'month', 'avg_sentiment']

    # Pivot the table to create a feature vector per country
    time_sentiment_pivot = time_sentiment.pivot(index='country', columns='month', values='avg_sentiment').fillna(0)

    return time_sentiment_pivot

def determine_optimal_clusters(time_sentiment, max_clusters=10):
    wcss = []
    for i in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, random_state=42)
        kmeans.fit(time_sentiment)
        wcss.append(kmeans.inertia_)

    # Find the "elbow point" where the rate of WCSS decrease slows down
    differences = [wcss[i - 1] - wcss[i] for i in range(1, len(wcss))]
    optimal_k = differences.index(max(differences)) + 2  # Adding 2 since index starts at 0 for the second cluster

    return optimal_k

def perform_clustering_with_time_features(time_sentiment, n_clusters):
    # Apply K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    time_sentiment['cluster'] = kmeans.fit_predict(time_sentiment)

    return time_sentiment.reset_index()

def visualize_clusters_with_time_features(clustered_data):
    # Use the first principal component as a proxy for visualization
    clustered_data['avg_sentiment'] = clustered_data.drop(columns=['country', 'cluster']).mean(axis=1)
    fig = px.scatter(
        clustered_data,
        x='avg_sentiment',
        y='cluster',
        text='country',
        color='cluster',
        title='Country Sentiment Clusters (with Time Features)',
        labels={'avg_sentiment': 'Average Sentiment', 'cluster': 'Cluster'},
    )
    fig.update_traces(textposition='top center')
    return fig

def process_dataset_with_time_features(df, max_clusters=10):
    time_sentiment = calculate_time_based_sentiment(df)
    optimal_k = determine_optimal_clusters(time_sentiment, max_clusters)
    print(f"Optimal number of clusters determined: {optimal_k}")
    clustered_data = perform_clustering_with_time_features(time_sentiment, optimal_k)
    fig = visualize_clusters_with_time_features(clustered_data)
    return fig

# To run the pipeline on a dataset:
# file_path = r"C:\Users\horac\OneDrive\Escritorio\headlines_repo.xlsx"
# result = process_dataset_with_time_features(file_path, max_clusters=4)
# print(result)