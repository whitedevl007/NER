# import urllib.request
# import io
# from slugify import slugify
# from bs4 import BeautifulSoup
# from pdfminer.high_level import extract_text
# import os

# SEED_URL = "https://joss.theoj.org/papers/published?page={page}"
# MAX_PAGE = 203
# pages = [SEED_URL.format(page=i+1) for i in range(0, MAX_PAGE)]
# print(f"{len(pages)} pages to crawl")

# documents = []
# for i, page in enumerate(pages, start=1):
#     try:
#         html_doc = io.BytesIO(urllib.request.urlopen(page).read())
#     except urllib.error.URLError as e:
#         print(f"Error {i}/{len(pages)}: {e}")
#         continue
#     soup = BeautifulSoup(html_doc, 'html.parser')
#     items = soup.find_all("h2", class_="paper-title")
#     for item in items:
#         a_tag = item.find("a", href=True)
#         if a_tag:
#             documents.append((slugify(a_tag.text), a_tag["href"]))
#     print(f"Crawled {i}/{len(pages)} pages")

# print(f"{len(documents)} documents found")
# print(documents[0])

# directory = "docs"
# os.makedirs(directory, exist_ok=True)

# for i, (slug, url) in enumerate(documents, start=1):
#     try:
#         filename_pdf = os.path.join(directory, f"{slug}.pdf")
#         filename_txt = os.path.join(directory, f"{slug}.txt")
#         url_pdf = f"{url}.pdf"
#         urllib.request.urlretrieve(url_pdf, filename_pdf)
#         with open(filename_txt, "w") as f:
#             text = extract_text(filename_pdf)
#             f.write(text)
#         print(f"Downloaded and extracted {i}/{len(documents)} documents")
#     except Exception as ex:
#         print(f"Error {i}/{len(documents)}: {url} {str(ex)}")






import urllib.request
import io
from slugify import slugify
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
import os

SEED_URL = "https://joss.theoj.org/papers/published?page={page}"
MAX_PAGE = 203
pages = [SEED_URL.format(page=i+1) for i in range(0, MAX_PAGE)]
print(f"{len(pages)} pages to crawl")

documents = []
for i, page in enumerate(pages, start=1):
    try:
        html_doc = io.BytesIO(urllib.request.urlopen(page).read())
    except urllib.error.URLError as e:
        print(f"Error {i}/{len(pages)}: {e}")
        continue
    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all("h2", class_="paper-title")
    for item in items:
        a_tag = item.find("a", href=True)
        if a_tag:
            documents.append((slugify(a_tag.text), a_tag["href"]))
    print(f"Crawled {i}/{len(pages)} pages")

print(f"{len(documents)} documents found")
print(documents[0])

directory = "docs"
os.makedirs(directory, exist_ok=True)

for i, (slug, url) in enumerate(documents, start=1):
    filename_pdf = os.path.join(directory, f"{slug}.pdf")
    if os.path.exists(filename_pdf):
        print(f"Skipping {i}/{len(documents)} documents (PDF already exists)")
        continue
    try:
        url_pdf = f"{url}.pdf"
        urllib.request.urlretrieve(url_pdf, filename_pdf)
        with open(os.path.join(directory, f"{slug}.txt"), "w") as f:
            text = extract_text(filename_pdf)
            f.write(text)
        print(f"Downloaded and extracted {i}/{len(documents)} documents")
    except Exception as ex:
        print(f"Error {i}/{len(documents)}: {url} {str(ex)}")
