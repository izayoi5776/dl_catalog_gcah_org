from encodings import utf_8
from genericpath import exists
import urllib
import os
import sys
import time
from bs4 import BeautifulSoup
from pathlib import Path

# eg https://catalog.gcah.org/images/collections/show/6
def get1url(url):
  with urllib.request.urlopen(url) as res:
    html = res.read()
    soup = BeautifulSoup(html, "html5lib")
    #$$('a.permalink')[1].href
    for i in soup.select("a.permalink"):
      #print(urllib.parse.urljoin(url, i["href"]))
      getlvl2url(urllib.parse.urljoin(url, i["href"]))

# eg https://catalog.gcah.org/images/items/show/3337
def getlvl2url(url):
  print("url=" + url, end="")
  if(os.path.exists(os.path.basename(url) + ".html")):
    print("...SKIP")
  else:
    print("...")
    with urllib.request.urlopen(url) as res:
      html = res.read()
      soup = BeautifulSoup(html, "html5lib")
      # image
      for i in soup.select("div#item-images a"):
        getFile(urllib.parse.urljoin(url, i["href"]))
      # thumbnails
      for i in soup.select("div#item-images a img"):
        getFile(urllib.parse.urljoin(url, i["src"]))
      for i in soup.select("link"):
        try:
          getFile(urllib.parse.urljoin(url, i["href"]))
        except:
          continue
      for i in soup.select("script"):
        try:
          getFile(urllib.parse.urljoin(url, i["src"]))
        except:
          continue
      
      rewriteHtml(url, soup)

# 重写html
def rewriteHtml(url, soup):
    for i in soup.select("a"):
      i["href"] = url2relative(i["href"])
    for i in soup.select("img"):
      i["src"] = url2relative(i["src"])
    for i in soup.select("link"):
      i["href"] = url2relative(i["href"])
    for i in soup.select("script"):
      try:
        i["src"] = url2relative(i["src"])
      except:
        continue
    for i in soup.select("li#previous-item a"):
      i["href"] = os.path.basename(i["href"]) + ".html"
    for i in soup.select("li#next-item a"):
      i["href"] = os.path.basename(i["href"]) + ".html"
    
    writeHtmlFile(url, soup)

# URL改写成相对路径  
def url2relative(url):
  path = url
  try:
    path = urllib.parse.urlparse(url).path
    if path.startswith("/"):
      path = path[1:]
  except:
    pass
  return path

# eg https://catalog.gcah.org/images/files/original/b5d1859bda32cee341ef836646f476bc.jpg
def getFile(url):
  path = urllib.parse.urlparse(url).path
  if path.startswith("/"):
    path = path[1:]
  print(" path=" + path, end="")
  if(os.path.exists(path)):
    print("...SKIP")
  else:
    print("...GET")
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, path)
  
def writeHtmlFile(url, soup):
  path = urllib.parse.urlparse(url).path
  if path.startswith("/"):
    path = path[1:]
  if not path.endswith(".html"):
    path = path + ".html"
  path = os.path.basename(path)
  print(" path=" + path, end="")
  if(os.path.exists(path)):
    print("...SKIP")
  else:
    print("...GET")
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
      f.write(str(soup))

# INSTALL
# pip install bs4
# pip install html5lib

# --- MAIN ----
urls = (
"https://catalog.gcah.org/images/collections/show/6",
"http://catalog.gcah.org/images/collections/show/7",
"https://catalog.gcah.org/images/collections/show/8",
"https://catalog.gcah.org/images/collections/show/9",
"https://catalog.gcah.org/images/collections/show/10",
"https://catalog.gcah.org/images/collections/show/11",
"https://catalog.gcah.org/images/collections/show/12",
"https://catalog.gcah.org/images/collections/show/2",
"https://catalog.gcah.org/images/collections/show/3",
"https://catalog.gcah.org/images/collections/show/4",
"https://catalog.gcah.org/images/collections/show/5",
"https://catalog.gcah.org/images/collections/show/19",
"https://catalog.gcah.org/images/collections/show/18",
"https://catalog.gcah.org/images/collections/show/20",
"https://catalog.gcah.org/images/collections/show/21",
"https://catalog.gcah.org/images/collections/show/22",
"https://catalog.gcah.org/images/collections/show/24",
"https://catalog.gcah.org/images/collections/show/25",
"https://catalog.gcah.org/images/collections/show/26",
"https://catalog.gcah.org/images/collections/show/28",
"https://catalog.gcah.org/images/collections/show/29",
"https://catalog.gcah.org/images/collections/show/31",
)
for url in urls:
  get1url(url)
