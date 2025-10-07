"""
All data scraped from Detective Conan World (https://www.detectiveconanworld.com/).
Project is used for non-commercial, educational purposes and is unaffiliated with DCW.
"""


from bs4 import BeautifulSoup
import requests

URL = "https://www.detectiveconanworld.com/wiki/Anime#Episodes"

headers = {
    "Accept-Language": "en-GB,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
}

page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")

content = soup.find("div", class_="mw-parser-output")
season_tables = content.find_all("table", class_="wikitable") # only include the first 30 tables as there are only 30 seasons so far

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
print(black_org_episodes)