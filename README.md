# world_news_monitor



#Git Commands
git clone https://github.com/hasalamanca/world_news_monitor.git
cd .\world_news_monitor\
git status
git add main.py
git push origin main
git commit -m "Adding main .py"
git config --global user.name "hasalamanca"
git config --global user.email "hasalamanca@student.ie.edu"
git push origin main
git fetch
git pull



#Design of pieces

Make functions of all pieces.

1) Retrieve news headlines and store them

2) Generate master table describing: id, headline, country, outlet, category.

3) Translate headline to english, attach result to table as headline_eng

4) Headline sentiment analysis, identify sentiment categories and attach result as a column to the table as sentiment_category.

5) Generate visualization tables, considering:
    a) country, news_category, news_category% (number of news of the category/number of all news), sentiment_category, sentiment_% (number of news of the sentiment/number of all news).

    b) News outlet, main_category, main_category%, main_sentiment, main_sentiment%

Plotly Dashboard will need to display:
1) A world map that changes color based on: 
    a) Predominant news categories per country
    b) Predominant sentiment per outlet

2) Summary table for all news (limit 50) sorted by latest first: timestamp,outlet, country, headline.

3) Summary table with the top 5 per the filtered category, separate table with the same with the top 5 filtered by sentiment. We leave a filter with a default value "Politics" and the other "Happy", and the user can choose the top 5 they want to look into.

CMND line implementation:
1) Intall and schedule the program to update once a day at 00:00 or upon restart of the system.
2) Have a command to unsinstall and unschedule.
3) If possible have an icon to start, else, run with a command line command.

Database:
1) SQLite and/or Github solution to retrieve and push data. Only the large source table should be stored and the rest calculated when excecuting the program. Through the id we will need to update only the new entries to the DB.