from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import sys
import time
import shutil

class Scrape:
    def __init__(self, url):
        self.url = url

    def start_scrape(self, url_page):
        page_res = requests.get(url_page)
        page_content = page_res.content
        soup = BeautifulSoup(page_content, features='html.parser')

        return soup

    def download_link(self):
        print "Start scrape to get zippyshare hosting download link"
        data = {}

        # start scrape
        soup = self.start_scrape(self.url)

        # download link lists
        soup_url_lists = soup.find_all("div", "downloadcloud")
        
        for tag in soup_url_lists:
            title = tag.find("h2").string.strip()
            zippyshare_links = tag.find_all("a", href=re.compile("zippyshare.com"))            
            try:
                data[title] = zippyshare_links[1].get("href") 
            except IndexError:
                print "Zippyshare not found"
            except:
                pass
        return data

    @staticmethod
    def get_zippyshare_movie_link(link):
        print "Start scrape movie link on zippyshare hosting"
        chromium_path = "/usr/lib/chromium-browser/chromedriver"

        driver = webdriver.PhantomJS()
        driver.implicitly_wait(10)

        driver.get(link)
        html = driver.page_source

        soup = BeautifulSoup(html, features='html.parser')

        get_movie_link = soup.find("a", {"id":"dlbutton"})
        print "Scrape Done"

        return get_movie_link.get("href")

def download(url_downlond=None):
    print "lol"
    download_hosting_domain = "https://www1.zippyshare.com"

    if url_downlond is None:
        print "url not provided"

    pattern = re.compile(r'^https$')
    for title, url in url_downlond.iteritems():
        filename = "{}.mkv".format(title)
        link = "{}{}".format("https:", url) 
        movie_link = "{domain}{movie}".format(domain=download_hosting_domain, movie=Scrape.get_zippyshare_movie_link(link))
        print "Tried to download {title}".format(title=title)   

        with requests.get(movie_link, stream=True) as r:
            print 'download started'
            with open(filenme, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
def main():

    url = "https://anikyojin.net/overlord-subtitle-indonesia-bd/"

    scrape = Scrape(url)

    downloads_url = scrape.download_link()
    print downloads_url
    download(downloads_url)

main()