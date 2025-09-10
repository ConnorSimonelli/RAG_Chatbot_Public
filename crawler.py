from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from collections import deque
from urllib.robotparser import RobotFileParser
import requests
import os
import time


def crawl(sight, maxPages):
    """
    Runner for web scraping, keeps track of what pages have been scrapped and what pages are next to scape.

    Input:
        sight: the user provided sight to crawl
        maxPages: the user provided max number of page to crawl
    
    """

    #Sets up rp, which stores robots.txt
    rp = setCheck(sight)
    
    #Checks to see if the sight can be scraped
    if check(sight, rp) == False:
        print("This website can't be scrape")
        return #Returns if the sight can not be scrapped
   
    toVisit = deque([sight]) #Adds sight to toVisit list
    visited = [] #Creates a list to keep track of webpages 
    domain = urlparse(sight).netloc #Get the domain from the url

    #Create a playwright section
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) #Define browser
        page = browser.new_page() #Create a new page on browser

        #If the toVisit is not empty and checks to make sure number of pages visited is not > then maxPages user provided
        while toVisit and len(visited) < maxPages:
            
            currentURL = toVisit.popleft() #Get the head of the toVisit List
            
            #Check to see if list currentURL has already be visited
            if currentURL in visited:
                continue
            #Check to see if the current url can be scrapped
            if check(currentURL, rp) == False:
                continue
            
            print(f"Crawling {currentURL}")#Indicate what page is being scrapped to the user
            soup = scrape(page, currentURL)#Scape webpage and save soup

            #Check is scrape has been success full
            if soup:
                saveSoup(soup, currentURL) #save soup as txt file
                getULRS(soup, currentURL, visited, toVisit, domain) #Get any URLS from the page
                visited.append(currentURL) #Add currentURL to visited list to prevent revisit
            
            time.sleep(3) #Wait 3 seconds to avoid overwhelming sever

        browser.close() #Once scraping is done close browser

    return

def scrape(page, url):
    """

    Scape the opened webpage and save it's html, if an error happens return None

    Input:
        page: browser page created by playwright
        url: URl for the webpage to scrape 

    Return:
        Returns html soup from url or None if error
        
    """

    try:
        page.goto(url, timeout=30000)
        page.wait_for_load_state("networkidle")
        html = page.content()
        return BeautifulSoup(html, "html.parser")
    except Exception as e:
        print(f"Error scraping {url}")
        return None


def getULRS(soup, currentURL, visited, toVisit, domain):
    """

    Analyzes html soup looking for urls to add to toVisit

    Input:
        soup: html soup for currentURl
        currentURL: the url of the webpage where the soup is from
        visited: a list of already visited sights
        toVisit: a list of sight the crawler will visit
        domain: the domain of the sight
        
    """

    for link in soup.find_all("a", href=True):
        fullURL = urljoin(currentURL, link['href'])
        # strip fragments (#about-us)
        fullURL = urlparse(fullURL)._replace(fragment="").geturl()
        if InternalURL(fullURL, domain) and fullURL not in visited and fullURL not in toVisit:
            toVisit.append(fullURL)


def InternalURL(url, domain):
    """



    """

    netloc = urlparse(url).netloc
    return netloc == domain or netloc == ''

def saveSoup(soup, currentURL):
    """



    """

    outputFolder = os.path.expanduser("./RAGData")
    safeFilename = currentURL.replace("https://", "").replace("http://", "").replace("/", "_").strip("_")
    filePath = os.path.join(outputFolder,f"{safeFilename}.txt")

    text = soup.get_text(separator=" ", strip=True)
    
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(text)

    return

def setCheck(url):
    """



    """

    robotURL = url+"/robots.txt"
    rp  = RobotFileParser()
    rp.set_url(robotURL)
    rp.read()

    return  rp


def check(url, rp):
    """



    """

    return rp.can_fetch("*", url)

    
