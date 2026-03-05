import requests
from bs4 import BeautifulSoup


def get_news():

    url = "https://www.bbc.com/news"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    # User-Agent: Siteye "Ben bir robot değilim, Chrome tarayıcısıyım" mesajı gönderir.
    # Bu olmazsa bazı siteler sizi hemen engeller.

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    news_data = []

    # haber başlıklarını bul
    headlines = soup.select('h2[data-testid="card-headline"]')

    for idx, headline in enumerate(headlines):

        # başlığın parentındaki linki bul, a h2 nin üstünde o yüzdem parent
        link_tag = headline.find_parent('a')

        if link_tag:
            title = headline.get_text(strip=True)
            #strip=True → baştaki ve sondaki boşlukları siler.
            url = link_tag.get("href")

            # link başında / varsa tam link yap
            if url.startswith("/"):
                url = "https://www.bbc.com" + url

            # sözlük olarak listeye ekle
            news_data.append({
                "id": idx + 1,
                "title": title,
                "url": url
            })

    return news_data


news = get_news()

for item in news[:10]:
    print(f"{item['id']}. {item['title']}")
    print(f"Link: {item['url']}\n")