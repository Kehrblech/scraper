import requests
from bs4 import BeautifulSoup
import json
import datetime
from urllib.parse import urlparse



#return raw html 
def get_soup(url):
    response = requests.get(url.encode('utf-8'))
    html = response.content

    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    return soup
    
#get table ADD parameter which
def table(soup):

    table = soup.find('table')

    data = []
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if columns:
            data.append([column.text.strip() for column in columns])
    return data
#get all tables
def all_tables(soup):
    tables = soup.find_all("table")
    # run trough all tables 
    table_data = []
    for table in tables:
        table_dict = []
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if columns:
                table_dict.append([column.text.strip() for column in columns])
        table_data.append(table_dict)
    return  json.loads(json.dumps(table_data))

def title_main(soup):
    title_main = soup.find("span", {"class": "mw-page-title-main"})
    return title_main    

#ADD which name
def title_h2(soup):
    title_h2 = soup.find("span", {"class": "mw-headline"})
    return title_h2

def all_title_h2(soup):
    all_h2_elements = soup.find_all("h2")
    h2_data = [] 
    for h2 in all_h2_elements:
        h2_data.append(h2.text)
    return  h2_data

def all_title_h3(soup):
    all_h3_elements = soup.find_all("h3")
    h3_data = [] 
    for h3 in all_h3_elements:
        h3_data.append(h3.text)
    return  h3_data

def titles_with_text(soup):
    all_h3_elements = soup.find_all("h3")
    h3_data = [] 
    for h3 in all_h3_elements:
        h3_data.append(h3.text)
    return  h3_data


#  Find paragraphs between start and end
def title_main_with_text(soup):
    # Find start tag
    h1_tag = soup.find('h1')
    # Find end tag
    toc_div = soup.find('div', {'id': 'toc'})
    # Find paragraphs between start(h1) and end('div', {'id': 'toc'}), in our case Headline and table of content
    paragraphs = []
    next_element = h1_tag.find_next()
    while next_element and next_element != toc_div:
        if next_element and next_element.name == 'p':
            paragraphs.append(next_element.text.strip())
        next_element = next_element.find_next()
    return paragraphs
#  Find paragraphs between start and end
def heading_h2_with_text_name_image(soup,start):
    
    h2_1 = soup.find('h2', text=start)

    # Find the second h2 tag
    h2_2 = h2_1.find_next_sibling('h2')
    
    # Find the paragraphs between h2 tags
    paragraphs = [h2_1.text.strip()]
    next_element = h2_1.find_next()
    while next_element != h2_2:
        if next_element and next_element.name == 'h3':
            paragraphs.append("<h3>"+next_element.text.strip())
        if next_element and next_element.name == 'img':
            paragraphs.append("<image-src>"+next_element["src"].strip())
        if next_element and 'thumbcaption' in next_element.attrs.get('class', []):
            #if 'magnify' not in next_element.attrs.get('class', []):
            paragraphs.append("<image-alt>" + next_element.text.strip())
        if next_element and next_element.name == 'p':
            paragraphs.append("<p>"+next_element.text.strip())
        next_element = next_element.find_next()     
    return paragraphs

def heading_h2_with_text_name(soup,start):
    h2_1 = soup.find('h2', text='Geographie')

    # Find the second h2 tag
    h2_2 = h2_1.find_next_sibling('h2')
    
    # Find the paragraphs between h2 tags
    paragraphs = [h2_1.text.strip()]
    next_element = h2_1.find_next()
    while next_element != h2_2:
        if next_element and next_element.name == 'h3':
            paragraphs.append("<h3>"+next_element.text.strip())
        if next_element and next_element.name == 'p':
            paragraphs.append("<p>"+next_element.text.strip())
        next_element = next_element.find_next()     
    return paragraphs
# Add image description
def image_from_heading_h2(soup):
    h2_1 = soup.find('h2', text='Name')
   
    # Find the second h2 tag
    h2_2 = h2_1.find_next('img')
    # Find the paragraphs between h2 tags
    return h2_2["src"]

def image_thumbs_all(soup):
    h1_1 = soup.find('div',{'id':'content'})
    #end = soup.find('h2', id='Weblinks')
    # Find the second h2 tag
    images_data = []
    images = h1_1.find_all('img')
    for image in images:
        images_data.append(image["src"])
    return images_data

def image_full_all(soup):
    h1_1 = soup.find('div',{'id':'content'})
    images_data = []
    images = h1_1.find_all('img')
    for image in images:
        if 'noprint' not in image.attrs.get('class', []) and not any('noprint' in c.get('class', []) for c in image.parents):
            parts = image["src"].split("/")
            parts.pop()
            full_image = "/".join(parts)
            final = full_image.replace("/thumb/", "/")
            images_data.append("https:"+final)
    return images_data
    

#  Find paragraphs between given start and end point
def heading_with_text_any(soup,start,end):
    # Find start tag
    h1_tag = soup.find(start)
    # Find end tag
    toc_div = soup.find(end)
    # Find paragraphs between start(h1) and end('div', {'id': 'toc'}), in our case Headline and table of content
    paragraphs = []
    next_element = h1_tag.find_next()
    while next_element and next_element != toc_div:
        if next_element and next_element.name == 'p':
            paragraphs.append(next_element.text.strip())
        next_element = next_element.find_next()
    return paragraphs

def heading_with_text_any(soup,start,end):
    # Find start tag
    h1_tag = soup.find(start)
    # Find end tag
    toc_div = soup.find(end)
    # Find paragraphs between start(h1) and end('div', {'id': 'toc'}), in our case Headline and table of content
    paragraphs = []
    next_element = h1_tag.find_next()
    while next_element and next_element != toc_div:
        if next_element and next_element.name == 'p':
            paragraphs.append(next_element.text.strip())
        next_element = next_element.find_next()
    return paragraphs

def table_of_contents_level_all_with_number(soup):
    toc = soup.find("div", {"id": "toc"})
    ul = toc.find("ul")
    lis = []
    data_li = ul.find_all('li')
    for toctext in data_li:
        element = toctext.find('span', {'class': 'tocnumber'}).get_text(strip=True)
        element += " " +toctext.find('span', {'class': 'toctext'}).get_text(strip=True)
        lis.append(element)
    return lis

def table_of_contents_level_all(soup):
    toc = soup.find("div", {"id": "toc"})
    ul = toc.find("ul")
    lis = []
    data_li = ul.find_all('li')
    for toctext in data_li:
        element = toctext.find('span', {'class': 'toctext'}).get_text(strip=True)
        lis.append(element)
    return lis

def table_of_contents_level_1(soup):
    toc = soup.find("div", {"id": "toc"})
    ul = toc.find("ul")
    lis = []
    data_li = ul.find_all('li', {'class': 'toclevel-1'})
    for toctext in data_li:
        lis.append(toctext.find('span', {'class': 'toctext'}).get_text(strip=True))
    return lis

def table_of_contents_level_2(soup):
    toc = soup.find("div", {"id": "toc"})
    ul = toc.find("ul")
    lis = []
    data_li = ul.find_all('li', {'class': 'toclevel-2'})
    for toctext in data_li:
        lis.append(toctext.find('span', {'class': 'toctext'}).get_text(strip=True))
    return lis

def table_of_contents_level_3(soup):
    toc = soup.find("div", {"id": "toc"})
    ul = toc.find("ul")
    lis = []
    data_li = ul.find_all('li', {'class': 'toclevel-3'})
    for toctext in data_li:
        lis.append(toctext.find('span', {'class': 'toctext'}).get_text(strip=True))
    return lis
def table_of_contents_level_4(soup):
    toc = soup.find("div", {"id": "toc"})
    ul = toc.find("ul")
    lis = []
    data_li = ul.find_all('li', {'class': 'toclevel-4'})
    for toctext in data_li:
        lis.append(toctext.find('span', {'class': 'toctext'}).get_text(strip=True))
    return lis

def table_of_contents_level_num(soup,num):
    toc = soup.find("div", {"id": "toc"})
    ul = toc.find("ul")
    lis = []
    data_li = ul.find_all('li', {'class': 'toclevel-'+num})
    for toctext in data_li:
        lis.append(toctext.find('span', {'class': 'toctext'}).get_text(strip=True))
    return lis
    
def search_results(soup):
    search_results = soup.find("ul", {"class": "mw-search-results"})
    return search_results


def get_date():
    return str(datetime.date.today()).strip()

##!! 
def heading_h2_with_text_name_image_auto(soup):
    counter_toc_data = 0 
    toc_data = table_of_contents_level_1(soup)
    end_number = len(toc_data) - 1
    content = soup.find('div',{'id':'content'})
    
    headings = []
    paragraphs = []
    
    while counter_toc_data < end_number:
        start = content.find('span', {'class': 'mw-headline'})
        if start:
            print(start,counter_toc_data)
            ueberschrift = start.text.strip()
            headings.append(ueberschrift)
            end = start.find_next_sibling('span', {'class': 'mw-headline'})
            print(end)
            next_element = start.find_next()
            print(ueberschrift)
            if end==None:
                print("end")
                break
            if next_element == None:
                print("end")
                break
            else:
                while next_element != end:
                    print(next_element)
                    if next_element and next_element.name == 'h3':
                        paragraphs.append("<h3>"+next_element.text.strip())
                    if next_element and next_element.name == 'img':
                        paragraphs.append("<image-src>"+next_element["src"].strip())
                    if next_element and 'thumbcaption' in next_element.attrs.get('class', []):
                        #if 'magnify' not in next_element.attrs.get('class', []):
                        paragraphs.append("<image-alt>" + next_element.text.strip())
                    if next_element and next_element.name == 'p':
                        paragraphs.append("<p>"+next_element.text.strip())
                    next_element = next_element.find_next()
        counter_toc_data += 1
    return paragraphs
##!!