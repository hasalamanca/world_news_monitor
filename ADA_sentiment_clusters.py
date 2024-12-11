import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px


def load_and_clean_data(file_path, sheet_name='headlines_repo'):
    """
    Load the dataset from an Excel file and clean the `publishedAt` column.

    Parameters:
    file_path (str): Path to the Excel file.
    sheet_name (str): Name of the sheet to load.

    Returns:
    pd.DataFrame: Cleaned DataFrame with `publishedAt` as a date-only column.
    """
    # Load the Excel sheet
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Parse 'publishedAt' column to datetime and extract only the date
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce', utc=True).dt.date

    return df

def calculate_country_sentiment(df):
    """
    Calculate the average sentiment for each country.

    Parameters:
    df (pd.DataFrame): Input DataFrame with `country` and `sentiment` columns.

    Returns:
    pd.DataFrame: DataFrame with average sentiment per country.
    """
    country_sentiment = df.groupby('country')['sentiment'].mean().reset_index()
    country_sentiment.columns = ['country', 'avg_sentiment']

    return country_sentiment

def calculate_time_based_sentiment(df):
    """
    Calculate the average sentiment for each country by time period (e.g., month).

    Parameters:
    df (pd.DataFrame): Input DataFrame with `country`, `publishedAt`, and `sentiment` columns.

    Returns:
    pd.DataFrame: DataFrame with time-based sentiment trends for clustering.
    """
    df['month'] = pd.to_datetime(df['publishedAt']).dt.to_period('M')
    time_sentiment = df.groupby(['country', 'month'])['sentiment'].mean().reset_index()
    time_sentiment.columns = ['country', 'month', 'avg_sentiment']

    # Pivot the table to create a feature vector per country
    time_sentiment_pivot = time_sentiment.pivot(index='country', columns='month', values='avg_sentiment').fillna(0)

    return time_sentiment_pivot

def determine_optimal_clusters(time_sentiment, max_clusters=10):
    """
    Automatically determine the optimal number of clusters using the Elbow Method.

    Parameters:
    time_sentiment (pd.DataFrame): Pivoted DataFrame with time-based features.
    max_clusters (int): Maximum number of clusters to evaluate.

    Returns:
    int: Optimal number of clusters based on the Elbow Method.
    """
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
    """
    Apply K-Means clustering using both average sentiment and time-based features.

    Parameters:
    time_sentiment (pd.DataFrame): Pivoted DataFrame with time-based features.
    n_clusters (int): Number of clusters to form.

    Returns:
    pd.DataFrame: DataFrame with cluster assignments for each country.
    """
    # Apply K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    time_sentiment['cluster'] = kmeans.fit_predict(time_sentiment)

    return time_sentiment.reset_index()

def visualize_clusters_with_time_features(clustered_data):
    """
    Create a scatter plot of the clusters with country labels and time-based features.

    Parameters:
    clustered_data (pd.DataFrame): DataFrame with cluster assignments and country data.

    Returns:
    None
    """
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
    fig.show()

def process_dataset_with_time_features(file_path, max_clusters=10):
    """
    Load, clean, and analyze a dataset to compute and visualize clusters with time-based features.

    Parameters:
    file_path (str): Path to the dataset.
    max_clusters (int): Maximum number of clusters to evaluate for the Elbow Method.

    Returns:
    pd.DataFrame: DataFrame with cluster assignments for each country.
    """
    df = load_and_clean_data(file_path)
    time_sentiment = calculate_time_based_sentiment(df)
    optimal_k = determine_optimal_clusters(time_sentiment, max_clusters)
    print(f"Optimal number of clusters determined: {optimal_k}")
    clustered_data = perform_clustering_with_time_features(time_sentiment, optimal_k)
    visualize_clusters_with_time_features(clustered_data)
    return clustered_data



# To run the pipeline on a dataset:
file_path = r"C:\Users\horac\OneDrive\Escritorio\headlines_repo.xlsx"
result = process_dataset_with_time_features(file_path, max_clusters=4)
print(result)
