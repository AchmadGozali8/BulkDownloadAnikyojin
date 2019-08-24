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

    def extract_html_content(self, url_page):
        page_res = requests.get(url_page)
        page_content = page_res.content
        soup = BeautifulSoup(page_content, features='html.parser')

        return soup

    def zippyshare_download_links(self):
        print "Start scrape to get zippyshare hosting download link"
        data = {}

        # start scrape
        soup = self.extract_html_content(self.url)

        # download link lists
        soup_url_lists = soup.find_all("div", "downloadcloud")
        
        total_episode = 13

        list_episode_only = total_episode - len(soup_url_lists)

        for tag in soup_url_lists[:list_episode_only]:
            print tag
            title = tag.find("h2").string.strip()
            zippyshare_links = tag.find_all("a", href=re.compile("zippyshare.com"))            

            try:
                data[title] = zippyshare_links[1].get("href") 
            except IndexError:
                print "Zippyshare not found"
            except:
                break
        print data
        return data

    @staticmethod
    def zippyshare_movie_link(link):
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

# def download(url_downlond=None):
#     download_hosting_domain = "https://www1.zippyshare.com"

#     if url_downlond is None:
#         print "url not provided"

#     pattern = re.compile(r'^https$')

#     for title, url in url_downlond.iteritems():
#         filename = "{}.mkv".format(title)
#         link = "{}{}".format("https:", url) 
#         movie_link = "{domain}{movie}".format(domain=download_hosting_domain, movie=Scrape.zippyshare_movie_link(link))
#         print "Tried to download {title}".format(title=title)   


def main():
    url = "https://anikyojin.net/overlord-subtitle-indonesia-bd/"
    scrape = Scrape(url)
    downloads_url = scrape.zippyshare_download_links()
    print downloads_url

main()