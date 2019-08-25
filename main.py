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
    def zippyshare_movie_link(link, title):
        print "======================================================================================"
        print "Start scrape movie link on zippyshare hosting"
        chromium_path = "/usr/lib/chromium-browser/chromedriver"

        driver = webdriver.PhantomJS()
        driver.implicitly_wait(10)

        driver.get("{}{}".format("https:", link))
        html = driver.page_source

        soup = BeautifulSoup(html, features='html.parser')

        get_movie_link = soup.find("a", {"id":"dlbutton"})
        print "Scrape {} Done".format(title)
        print "======================================================================================"

        return get_movie_link.get("href")


class SaveToLocal:

    @staticmethod
    def save_as_file(links=[], filename=""):
        download_hosting_domain = "https://www1.zippyshare.com"

        with open("{}.txt".format(filename), "wb") as f:
           for link in links:
               f.write("{domain}{link}".format(domain=download_hosting_domain, link=link))
               f.write("\n")

def main():
    url = "https://anikyojin.net/world-god-only-know-sub-indo-bd/"

    filename = url.split("/")[3] 

    scrape = Scrape(url)

    zippyshare_links = scrape.zippyshare_download_links()

    movie_links = [Scrape.zippyshare_movie_link(v, k) for k,v in zippyshare_links.iteritems()]

    save_to_file = SaveToLocal.save_as_file(movie_links, filename)

main()