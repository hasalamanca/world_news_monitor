# World News Monitor

[Project Design](#project-design)

[Installation](#installation)

[Usage](#usage)

## Project Design

News API: https://newsapi.org/docs

Data manipulation:

1. Retrieve news headlines

2. Generate master table with all structured data describing at least: id, headline, country, outlet. OK Sample Provided

3. Translate headline to english, attach result to table as headline_eng.

4. Headline sentiment analysis, identify sentiment categories and attach result as a column to the table as sentiment_category.

5. Generate visualization tables, considering:

    a. country, news_category, news_category% (number of news of the category/number of all news), sentiment_category, sentiment_% (number of news of the sentiment/number of all news).

    b. News outlet, main_category, main_category%, main_sentiment, main_sentiment%

Plotly Dashboard will need to display:
1. A world map that changes color based on: 

    a. Predominant news categories per country

    b. Predominant sentiment per outlet

2. Summary table for all news (limit 50) sorted by latest first: timestamp,outlet, country, headline.

3. Summary table with the top 5 per the filtered category, separate table with the same with the top 5 filtered by sentiment. We leave a filter with a default value "Politics" and the other "Happy", and the user can choose the top 5 they want to look into.

## Installation

Before using, dependencies need to be installed. You might want to create a virtual environment previously. 

Execute the following command:

```bash
pip install -r requirements.txt
```

## Usage

Before executing these commands, make sure you have a valid API key in your `.env` file with the variable `NEWS_API_KEY=your_api_key`. Do not include quotation marks if you are on Windows.

To fetch the latest news sources and headlines, execute:

```bash
python main.py update
```

To display the dashboard on a web browser:

```bash
streamlit run main.py visualize
```