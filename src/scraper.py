import urllib
import requests
from bs4 import BeautifulSoup as bs
from validator_collection import checkers

class Scraper:
    def __init__(self):
        self.rootURL = 'https://paperswithcode.com'
        self.trendingPapersURL = self.rootURL
        self.latestURL = 'https://paperswithcode.com/latest'
        self.greatestURL = 'https://paperswithcode.com/greatest'
        self.linkToPaperPage = None
        self.trendingPapers = None
        self.latestPapers = None
        self.greatestPapers = None

    def scrapTrending(self):
        req = requests.get(self.trendingPapersURL)
        soup = bs(req.text, 'lxml')

        self.trendingPapers = self.scrapPage(soup)

        return self.trendingPapers

    def scrapLatest(self):
        req = requests.get(self.latestURL)
        soup = bs(req.text, 'lxml')

        self.latestPapers = self.scrapPage(soup).copy()

        return self.latestPapers

    def scrapGreatest(self):
        req = requests.get(self.greatestURL)
        soup = bs(req.text, 'lxml')

        self.greatestPapers = self.scrapPage(soup).copy()

        return self.greatestPapers

    def scrapPage(self, soup):
        papers_dict = {}
        papers = []

        items_divs = soup.find_all('div', {'class':'row infinite-item item'})

        for item in items_divs:
            for child in item.children:
                # Image
                try:
                    # Check if classes are in child attributes
                    if set(child.attrs['class']) <= set(['col-lg-3', 'item-image-col']):
                        # Image url
                        #print(child.find('div', {'class':'item-image'})['style'])  
                        papers_dict['image'] = self.rootURL + str(child.find('div', {'class':'item-image'})['style'].split("('", 1)[1].split("')")[0])
                        #print(papers_dict['image'])
                except:
                    pass

                # Content
                try:
                    if set(child.attrs['class']) <= set(['col-lg-9', 'item-col']):
                        # Title
                        #print(child.find('h1').a.string)
                        papers_dict['title'] = child.find('h1').a.string
                        # Nb stars
                        #print(child.find('span', {'class':'badge badge-secondary'}).text.strip())
                        papers_dict['nb_stars'] = child.find('span', {'class':'badge badge-secondary'}).text.strip()
                        # Star/hour
                        #print(child.find('div', {'class':'stars-accumulated text-center'}).text.strip())
                        papers_dict['hourly_stars'] = child.find('div', {'class':'stars-accumulated text-center'}).text.strip();
                        # Paper page link link
                        #print(child.find('a', {'class':'badge badge-light'})['href'])
                        linkToPaperPage = child.find('a', {'class':'badge badge-light'})['href']
                except:
                    pass

            if linkToPaperPage != None:
                req = requests.get(self.rootURL + linkToPaperPage)
                linkToPaperPage = None
                soup = bs(req.text, 'lxml')
                #print(soup.find('a', {'class':'badge badge-light'})['href'])
                pdf_link = soup.find('a', {'class':'badge badge-light'})['href']
                # Check if the link found is the pdf or a search query
                if checkers.is_url(pdf_link):
                    r = requests.get(pdf_link)
                else:
                    r = requests.get(self.rootURL + pdf_link)
                
                content_type = r.headers.get('content-type')

                if 'application/pdf' in content_type:
                    papers_dict['pdf'] = pdf_link
                    # Github link
                    #print(soup.find('a', {'class':'code-table-link'})['href'])
                    papers_dict['github'] = soup.find('a', {'class':'code-table-link'})['href']
                elif 'text/html' in content_type:
                    soup = bs(r.text, 'lxml')
                    # PDF link
                    #print(soup.find('a', {'class':'badge badge-light'})['href'])
                    papers_dict['pdf'] = soup.find('a', {'class':'badge badge-light'})['href']
                    # Github link
                    #print(soup.find('a', {'class':'code-table-link'})['href'])
                    papers_dict['github'] = soup.find('a', {'class':'code-table-link'})['href']
            
            papers.append(papers_dict.copy())
        return papers