import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import hashlib

# 🔍 Tes recherches personnalisées
SEARCHES = [
    {
        "name": "Salopettes",
        "queries": [
            "salopette dickies",
            "salopette carhartt",
            "salopette levis",
            "salopette vintage"
        ],
        "price_min": 15,
        "price_max": 50
    },
    {
        "name": "Surf & Skate",
        "queries": [
            "tshirt vintage surf",
            "tee shirt skate usa",
            "sweat vintage hawaii",
            "pull vintage australie"
        ],
    },
    {
        "name": "Dr Martens",
        "queries": [
            "dr martens"
        ],
        "price_max": 100
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def generate_url(query, price_min=None, price_max=None):
    url = f"https://www.vinted.fr/vetements?search_text={query.replace(' ', '+')}"
    if price_min:
        url += f"&price_from={price_min}"
    if price_max:
        url += f"&price_to={price_max}"
    return url

def hash_item(link):
    return hashlib.md5(link.encode()).hexdigest()

def load_previous_results():
    try:
        with open("articles.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_results(results):
    with open("articles.json", "w") as f:
        json.dump(results, f, indent=2)

def extract_articles_from_page(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("div.feed-grid__item a[href^='/items/']")
    articles = []

    for item in items:
        title = item.get("title") or "Sans titre"
        link = "https://www.vinted.fr" + item["href"]
        article_id = hash_item(link)

        articles.append({
            "id": article_id,
            "title": title,
            "url": link,
            "timestamp": datetime.utcnow().isoformat()
        })

    return articles

def run_tracker():
    print("🔍 Lancement de la veille Vinted...")

    previous = load_previous_results()
    all_results = {}

    for search in SEARCHES:
        search_name = search["name"]
        all_results[search_name] = []

        for query in search["queries"]:
            url = generate_url(query, search.get("price_min"), search.get("price_max"))
            print(f"🧭 Requête : {url}")
            res = requests.get(url, headers=HEADERS)
            if res.status_code != 200:
                print(f"❌ Erreur requête {url}")
                continue

            new_articles = extract_articles_from_page(res.text)

            for article in new_articles:
                if article["id"] not in previous.get(search_name, []):
                    print(f"🆕 Nouvel article trouvé : {article['title']}")
                    all_results[search_name].append(article)

            # Ajout de l'historique
            if search_name not in previous:
                previous[search_name] = []

            previous[search_name].extend([a["id"] for a in all_results[search_name]])

    save_results(previous)
    print("✅ Veille terminée.")

if __name__ == "__main__":
    run_tracker()
