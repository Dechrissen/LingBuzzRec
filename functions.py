import random
import requests
from bs4 import BeautifulSoup, NavigableString
import re
#import tensorflow as tf

class Paper():
    def __init__(self, title, link, authors, abstract, keywords):
        assert type(title) is str
        assert type(link) is str
        assert type(authors) is list
        for author in authors:
            assert type(author) is str
        assert type(abstract) is str
        assert type(keywords) is list
        for keyword in keywords:
            assert type(keyword) is str
        self.title = title
        self.link = link
        self.authors = authors
        self.abstract = abstract
        self.keywords = keywords

def scrapeLingBuzzHomePage():
    """Scrapes LingBuzz homepage for new papers to extract title, link to paper,
     authors, abstract, and keywords. Creates a new Paper object for each new
     upload."""

    # Get LingBuzz homepage
    homepage = requests.get('https://ling.auf.net/lingbuzz/')
    soup = BeautifulSoup(homepage.content, 'html.parser')
    # Sequentially work down to the table that stores first page of papers
    html = list(soup.children)[1]
    body = list(html.children)[1]
    main_table = list(body.children)[2]
    tbody = list(main_table.children)[0]
    tr = list(tbody.children)[0]
    td_1 = list(tr.children)[0]

    # Store html table of entire first page of papers in recent_papers_table
    # Each element in this list is of class 'bs4.element.Tag'
    # Each element (paper) is a <tr>
    # Each <tr> is comprised of 4 <td> tags containing: Authors, Newness, PDF link, Title
    recent_papers_table = list(td_1.children)
    n = 7 # number of the paper to find
    # Authors
    authors = []
    authors_td = list(list(recent_papers_table[n].children)[0].children)
    for tag in authors_td:
        if tag.name == 'a':
            authors.append(tag.get_text())

    # Newness
    newness_td = list(list(recent_papers_table[n].children)[1].children)[0]
    if isinstance(newness_td, NavigableString):
        print("Newness: None") # eventually ignore this entry if there are no children (i.e. a singular <b>)
    else:
        print("Newness:", list(newness_td.children)[0])

    # PDF link
    pdf_td = list(list(recent_papers_table[n].children)[2].children)[0]
    pdf_link = 'https://ling.auf.net' + pdf_td['href']

    # Link to summary
    summary_td = list(list(recent_papers_table[n].children)[3].children)[0]
    summary_link = 'https://ling.auf.net' + summary_td['href']

    # Title
    title = summary_td.get_text()

    # Abstract
    # Use summary link to get a paper's page
    page = requests.get(summary_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Sequentially work down to the paper's abstract
    html = list(soup.children)[1]
    body = list(html.children)[1]
    # The abstract is at the 5th index of the body's children list
    abstract = str(list(body.children)[5])

    # Keywords
    keywords_tr = list(list(body.children)[6].children)[3]
    keywords_list_td = list(keywords_tr.children)[1]
    keywords = keywords_list_td.get_text()
    keywords = re.split(r'[,|;]', keywords)
    keywords = [k.strip() for k in keywords]

    # Construct Paper object
    current_paper = Paper(title, pdf_link, authors, abstract, keywords)

    # Tests
    print(current_paper.title)
    print(current_paper.link)
    print(current_paper.authors)
    print(current_paper.abstract)
    print(current_paper.keywords)

def queryLingBuzz(query):
    """Takes a query and returns a list of Paper objects resulting from that
    query on LingBuzz.

    Parameters
    ----------
    query : string
        The string to query LingBuzz with.

    Returns
    -------
    list
        List of Paper objects.

    """
    # Get LingBuzz search results page according to `query`
    page = requests.get(f'https://ling.auf.net/lingbuzz/_search?q={query}')
    soup = BeautifulSoup(page.content, 'html.parser')
    # Sequentially work down to the table that stores first page of papers
    html = list(soup.children)[1]
    body = list(html.children)[1]
    main_table = list(body.children)[0]

    #print('whole table:', main_table)

    #first_cell = list(main_table.children)[0]
    #td_1 = list(first_cell.children)[0] #gets authors of first paper
    #print(td_1)

    # Store html table of entire first page of papers in main_table
    # Each element in this list is of class 'bs4.element.Tag'
    # Each element (paper) is a <tr>
    # Each <tr> is comprised of 4 <td> tags containing: NULL, Authors, Newness, Title (link to summary)
    n = 0 # number of the paper to find
    # Authors
    authors = []
    authors_td = list(list(list(main_table.children)[n].children)[0].children)[0]
    for tag in authors_td:
        if tag.name == 'a':
            authors.append(tag.get_text())
    print(authors)

    # Newness
    newness_td = list(list(list(main_table.children)[n].children)[0].children)[1]
    if isinstance(newness_td, NavigableString):
        print("Newness: None") # eventually ignore this entry if there are no children (i.e. a singular <b>)
    else:
        print("Newness:", list(newness_td.children)[0])


    # Link to summary
    summary_td = list(list(list(list(main_table.children)[n].children)[0].children)[2].children)[0]
    print(summary_td)
    summary_link = 'https://ling.auf.net' + summary_td['href']

    # Title
    title = summary_td.get_text()

    pdf_link = "http:fakelink"

    # Abstract
    # Use summary link to get a paper's page
    page = requests.get(summary_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Sequentially work down to the paper's abstract
    html = list(soup.children)[1]
    body = list(html.children)[1]
    # The abstract is at the 5th index of the body's children list
    abstract = str(list(body.children)[5])

    # Keywords
    keywords_tr = list(list(body.children)[6].children)[3]
    keywords_list_td = list(keywords_tr.children)[1]
    keywords = keywords_list_td.get_text()
    keywords = re.split(r'[,|;]', keywords)
    keywords = [k.strip() for k in keywords]

    # Construct Paper object
    current_paper = Paper(title, pdf_link, authors, abstract, keywords)

    # Tests
    print(current_paper.title)
    print(current_paper.link)
    print(current_paper.authors)
    print(current_paper.abstract)
    print(current_paper.keywords)



def classifier(text):
    """Returns a random (for now) binary classification value for a given text.

    Parameters
    ----------
    text : the text to be classified

    Returns
    -------
    bool
    """
    return random.choice([True, False])



# Run tests
#scrapeLingBuzzHomePage()
queryLingBuzz('word')
