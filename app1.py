from encodings import utf_8
from genericpath import exists
import urllib
import os
import sys
import time
from bs4 import BeautifulSoup
from pathlib import Path
import json

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
  id = url.split("/")[-1]
  if(os.path.exists(os.path.basename(url) + ".html")):
    print("...SKIP")
  else:
    print("...")
    with urllib.request.urlopen(url) as res:
      html = res.read()
      soup = BeautifulSoup(html, "html5lib")
      # image
      for i in soup.select("div#item-images a"):
        getFile(urllib.parse.urljoin(url, i["href"]), id)
        i["href"] = rewriteUrl(i["href"], id)
      # thumbnails
      for i in soup.select("div#item-images a img"):
        getFile(urllib.parse.urljoin(url, i["src"]), id)
        i["src"] = rewriteUrl(i["src"], id)
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

      buildJson(soup, id)
      rewriteHtml(soup, id)

# 保存 json 文件
def buildJson(soup, id):
  ret = {}
  ret["id"] = id
  for i in soup.select("h3"):
    ret[i.text] = i.parent.div.text
  print(ret)
  path = "json/" + id + ".json"
  Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
  with open(path, "w", encoding="utf-8") as f:
    f.write(json.dumps(ret, indent=2, ensure_ascii=False))
  return ret

# 把 url 重写成 id 
def rewriteUrl(url, id):
  newurl = url
  path = urllib.parse.urlparse(url).path
  ext = path.split(".")[-1]
  if path.startswith("/"):
    path = path[1:]
  newurl = os.path.dirname(path) + "/" + id + "." + ext
  return newurl

# 重写html
def rewriteHtml(soup, id):
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
    
    writeHtmlFile(soup, id)

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
#    id=3337
# 保存 url 对应文件，带目录结构，按照 id 改名
def getFile(url, id=None):
  path = urllib.parse.urlparse(url).path
  ext = path.split(".")[-1]
  if path.startswith("/"):
    path = path[1:]
  if id:
    path = os.path.dirname(path) + "/" + id + "." + ext
  print(" path=" + path, end="")
  if(os.path.exists(path)):
    print("...SKIP")
  else:
    print("...GET")
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, path)

# 保存 html 文件
def writeHtmlFile(soup, id):
  path = id + ".html"
  print(" path=" + path, end="")
  if(os.path.exists(path)):
    print("...SKIP")
  else:
    print("...GET")
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
#getlvl2url("https://catalog.gcah.org/images/items/show/3337")