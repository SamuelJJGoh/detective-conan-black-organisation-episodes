"""
All the data was scraped from Detective Conan World (https://www.detectiveconanworld.com/).
Project is used for non-commercial, educational purposes only and is unaffiliated with DCW.

This project produces two CSVs: 
- black_org_episodes.csv has all the episodes involving the black organisation in Detective Conan 
- total of 109 episodes

- non_remastered_black_org_episodes.csv has all the episodes involving the black organisation but excludes 
  any episodes that were remastered or reran
- total of 87 episodes

The csv files produced and the number of episodes in each file is as of 7th October 2025.
"""


from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = "https://www.detectiveconanworld.com/wiki/Anime#Episodes"

headers = {
    "Accept-Language": "en-GB,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
}

page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")

content = soup.find("div", class_="mw-parser-output")
season_tables = content.find_all("table", class_="wikitable") 

black_org_episodes = []

for season in season_tables:
    tbody = season.find("tbody")
    rows = tbody.find_all("tr") # rows is all the episodes in that season
    if not rows:
        continue

    # first row is just header for each season
    for tr in rows[1:]: # each tr is one episode
        tds = tr.find_all("td") # all td are part of one episode
        if not tds:
            continue
        
        episode_url = tr.find("a").get("href")

        # some episodes don't have a plot icon (don't have tds[5])
        plot = [img.get("alt") for img in (tds[5].find_all("img", alt=True) if len(tds) > 5 else [])]
        if "Black Organization" in plot:
            black_org_episodes.append({"episode_no": tds[0].getText(strip=True), 
                                       "title": tds[2].getText(strip=True),
                                       "air_date": tds[3].getText(strip=True),
                                       "episode_url": f"https://www.detectiveconanworld.com{episode_url}"})

# keep only episodes that have aired not future episodes
black_org_episodes = [e for e in black_org_episodes if e.get("air_date")]

# remove remastered and reran episodes
non_remastered_black_org_episodes = [
    e for e in black_org_episodes 
    if all(s not in (e.get("title")) for s in ("Remastered", "TV Special"))]

df = pd.DataFrame(black_org_episodes)[["episode_no", "title", "air_date", "episode_url"]]
df.to_csv("black_org_episodes.csv", index=False, encoding="utf-8-sig")

non_remastered_df = pd.DataFrame(non_remastered_black_org_episodes)[["episode_no", "title", "air_date", "episode_url"]]
non_remastered_df.to_csv("non_remastered_black_org_episodes.csv", index=False, encoding="utf-8-sig")