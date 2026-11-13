import time
import csv
import re
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/"
}

urls_file = open("urls.txt", "r")
urls = urls_file.readlines()
urls_file.close()

books_file = open('books.csv', 'w', newline='')
writer = csv.writer(books_file)
writer.writerow(['authors', 'title', 'year', 'like_count', 'book_tags', 'total_reads'])

for i in range(30):
    URL = urls[i].strip()
    page = requests.get(URL, headers=headers)
    row = []
    
    if page.status_code != 200:
        print(
            f"Failed to fetch page {i}. Status code: {page.status_code}. Stopping"
            " here."
        )
        break
    
    soup = BeautifulSoup(page.content, "html.parser")
    
    try:
        author = soup.find(class_="authors").text
    except:
        author = "None"
    row.append(author)
    
    try:
        title = soup.find(class_="head_title").find(class_="item").text
        #cleaning the title from zero width space characters
        title = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", title)
    except:
        title = "None"
    row.append(title)
    
    try:
        year = soup.find(class_="book_data").find_all("a")[1].text
    except:
        year = "None"
    row.append(year)
    
    try:
        like_count = soup.find(class_="like_count").text
    except:
        like_count = "None"
    row.append(like_count)

    # book tags
    book_tags_container = soup.find(id="book_tags")
    tags_list = []
    if book_tags_container:
        tag_elements = book_tags_container.find_all(class_="tag")
        
        tags_list = [t.text for t in tag_elements]

    # if no tags are found, store None
    tags_string = ", ".join(tags_list) if tags_list else "None"

    row.append(tags_string)
    
    
    print(f"Successfully read url {i + 1}:")
    writer.writerow(row)
    
    time.sleep(3)

books_file.close()
print("Task completed successfully!")

