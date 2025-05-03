import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Scrape IMDB Top 250
url = "https://www.imdb.com/chart/top/"
headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
movies = soup.select("tbody.lister-list tr")

movie_data = []
for movie in movies:
    title_column = movie.find("td", class_="titleColumn")
    rating_column = movie.find("td", class_="ratingColumn imdbRating")

    title = title_column.a.text
    year = int(title_column.span.text.strip("()"))
    rating = float(rating_column.strong.text)
    link = "https://www.imdb.com" + title_column.a['href']

    movie_data.append({
        "Title": title,
        "Year": year,
        "Rating": rating,
        "Link": link
    })

df = pd.DataFrame(movie_data)
df.to_csv("imdb_top_250.csv", index=False)
print("Scraped data saved to imdb_top_250.csv")

# Step 2: Visualization
plt.figure(figsize=(12, 6))
sns.histplot(df["Year"], bins=30, kde=False)
plt.title("Distribution of IMDB Top 250 Movies by Year")
plt.xlabel("Year")
plt.ylabel("Number of Movies")
plt.tight_layout()
plt.savefig("movies_by_year.png")
plt.show()

top_rated = df.sort_values(by="Rating", ascending=False).head(10)
plt.figure(figsize=(12, 6))
sns.barplot(data=top_rated, y="Title", x="Rating", palette="viridis")
plt.title("Top 10 IMDB Movies by Rating")
plt.xlabel("IMDB Rating")
plt.ylabel("Movie Title")
plt.tight_layout()
plt.savefig("top_10_movies.png")
plt.show()
