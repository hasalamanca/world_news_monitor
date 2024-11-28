# world_news_monitor

#Project Design

News API: https://newsapi.org/docs

Data manipulation:

1) Retrieve news headlines. OK 

2) Generate master table with all structured data describing at least: id, headline, country, outlet. OK Sample Provided

3) Translate headline to english, attach result to table as headline_eng.

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





## Manual: Managing a GitHub Repository

---

### **Section 1: How to Install the Repository in a Given Folder**

1. **Ensure Git is Installed**
   - Verify Git is installed on your system by running:
     ```powershell
     git --version
     ```
   - If Git is not installed, download and install it from [git-scm.com](https://git-scm.com/).

2. **Identify Yourself as a Git User**
   - Set your name and email for Git commits:
     ```powershell
     git config --global user.name "YourFullName"
     git config --global user.email "YourEmail@example.com"
     ```
   - Replace `"YourFullName"` and `"YourEmail@example.com"` with your name and email.

3. **Navigate to the Desired Folder**
   - Open PowerShell and move to the parent directory where you want to clone the repository:
     ```powershell
     cd "Path\To\Desired\Folder"
     ```
   - Replace `"Path\To\Desired\Folder"` with the folder’s path.

4. **Clone the Repository**
   - Run the following command to clone the repository into the folder:
     ```powershell
     git clone https://github.com/hasalamanca/world_news_monitor.git
     ```
   - The repository will be downloaded as a subfolder named `world_news_monitor` by default.

5. **(Optional) Clone into a Specific Folder**
   - If you want the repository in a specific folder, specify the target folder name:
     ```powershell
     git clone https://github.com/hasalamanca/world_news_monitor.git "C:\Path\To\Target\Folder"
     ```

6. **Navigate into the Repository Folder**
   - After cloning, move into the repository directory:
     ```powershell
     cd "world_news_monitor"
     ```

---

### **Section 2: How to Sync the Folder with GitHub**

1. **Navigate to the Repository Folder**
   - Ensure you are in the correct directory:
     ```powershell
     cd "Path\To\Repository\Folder"
     ```
   - Replace `"Path\To\Repository\Folder"` with your repository’s path.

2. **Check the Status of the Repository**
   - Review changes and ensure your local repository is up-to-date:
     ```powershell
     git status
     ```

3. **Stage All Changes**
   - Add all modified or new files to the staging area:
     ```powershell
     git add .
     ```

4. **Commit the Changes**
   - Save the staged changes to the local repository with a meaningful message:
     ```powershell
     git commit -m "Your commit message"
     ```

5. **Pull the Latest Changes from GitHub**
   - Update your local repository with any changes from the remote repository:
     ```powershell
     git pull origin main
     ```

6. **Push Local Changes to GitHub**
   - Send your committed changes to the remote repository:
     ```powershell
     git push origin main
     ```

7. **Verify the Sync**
   - Run the `git status` command again to ensure there are no pending changes.
