import time
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

f = open("urls.txt", "w")
for i in range(1, 4):
    URL = f"https://moly.hu/konyvek/osszes?page={i}"
    page = requests.get(URL, headers=headers)
    
    if page.status_code != 200:
        print(
            f"Failed to fetch page {i}. Status code: {page.status_code}. Stopping"
            " here."
        )
        break
    
    soup = BeautifulSoup(page.content, "html.parser")
    titles = soup.find_all(class_="fn book_selector")
    for title in titles:
        f.write("https://moly.hu" + title['href'] + "\n")
    
    print(f"Successfully scraped page {i}")
    
    time.sleep(2)

f.close()

print("Task completed successfully!")