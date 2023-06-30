import requests
from bs4 import BeautifulSoup
import json
import datetime
from urllib.parse import urlparse
import re
from urllib.parse import unquote

# return raw html
def get_soup(url):
    # decoded_url = unquote(url)
    # response = requests.get(decoded_url)
    response = requests.get(url.encode('utf-8'))
    html = response.content
    
    if response.status_code == 403:
        return "403 Forbidden"+str(Exception)
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    return soup

# get table ADD parameter which


def table(soup):

    table = soup.find('table')

    data = []
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if columns:
            data.append([column.text.strip() for column in columns])
    return data
# get all tables


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
    return json.loads(json.dumps(table_data, ensure_ascii=False))


def title_string(soup):
    title_text = soup.find()
    return
    


#Wiki Only
def title_main_wiki(soup):
    title_main = soup.find("span", {"class": "mw-page-title-main"})
    return title_main

# ADD which name


def title_h2(soup):
    title_h2 = soup.find("span", {"class": "mw-headline"})
    return title_h2


def all_title_h2(soup):
    all_h2_elements = soup.find_all("h2")
    h2_data = []
    for h2 in all_h2_elements:
        h2_data.append(h2.text)
    return h2_data


def all_title_h3(soup):
    all_h3_elements = soup.find_all("h3")
    h3_data = []
    for h3 in all_h3_elements:
        h3_data.append(h3.text)
    return h3_data


def titles_with_text(soup):
    all_h3_elements = soup.find_all("h3")
    h3_data = []
    for h3 in all_h3_elements:
        h3_data.append(h3.text)
    return h3_data


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


def heading_h2_with_text_name_image(soup, start):

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
            # if 'magnify' not in next_element.attrs.get('class', []):
            paragraphs.append("<image-alt>" + next_element.text.strip())
        if next_element and next_element.name == 'p':
            paragraphs.append("<p>"+next_element.text.strip())
        next_element = next_element.find_next()
    return paragraphs


def heading_h2_with_text_name(soup, start):
    h2_1 = soup.find('h2', text=start.strip())

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
    h1_1 = soup.find('div', {'id': 'content'})
    #end = soup.find('h2', id='Weblinks')
    # Find the second h2 tag
    images_data = []
    images = h1_1.find_all('img')
    for image in images:
        images_data.append(image["src"])
    return images_data


def image_full_all(soup):
    h1_1 = soup.find('div', {'id': 'content'})
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
def heading_with_text_any(soup, start, end):
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


def heading_with_text_any(soup, start, end):
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
        element = toctext.find(
            'span', {'class': 'tocnumber'}).get_text(strip=True)
        element += " " + \
            toctext.find('span', {'class': 'toctext'}).get_text(strip=True)
        lis.append(element)
    return lis


def table_of_contents_level_all(soup):
    toc = soup.find("div", {"id": "toc"})
    ul = toc.find("ul")
    lis = []
    data_li = ul.find_all('li')
    for toctext in data_li:
        element = toctext.find(
            'span', {'class': 'toctext'}).get_text(strip=True)
        lis.append(element)
    return lis


def table_of_contents_level_1(soup):
    toc = soup.find("div", {"id": "toc"})
    ul = toc.find("ul")
    lis = []
    data_li = ul.find_all('li', {'class': 'toclevel-1'})
    for toctext in data_li:
        lis.append(toctext.find(
            'span', {'class': 'toctext'}).get_text(strip=True))
    return lis


# def table_of_contents_level_2(soup):
#     toc = soup.find("div", {"id": "toc"})
#     ul = toc.find("ul")
#     lis = []
#     data_li = ul.find_all('li', {'class': 'toclevel-2'})
#     for toctext in data_li:
#         lis.append(toctext.find(
#             'span', {'class': 'toctext'}).get_text(strip=True))
#     return lis


# def table_of_contents_level_3(soup):
#     toc = soup.find("div", {"id": "toc"})
#     ul = toc.find("ul")
#     lis = []
#     data_li = ul.find_all('li', {'class': 'toclevel-3'})
#     for toctext in data_li:
#         lis.append(toctext.find(
#             'span', {'class': 'toctext'}).get_text(strip=True))
#     return lis


# def table_of_contents_level_4(soup):
#     toc = soup.find("div", {"id": "toc"})
#     ul = toc.find("ul")
#     lis = []
#     data_li = ul.find_all('li', {'class': 'toclevel-4'})
#     for toctext in data_li:
#         lis.append(toctext.find(
#             'span', {'class': 'toctext'}).get_text(strip=True))
    return lis


def table_of_contents_level_num(soup, num):
    toc = soup.find("div", {"id": "toc"})
    ul = toc.find("ul")
    lis = []
    data_li = ul.find_all('li', {'class': 'toclevel-'+num})
    for toctext in data_li:
        lis.append(toctext.find(
            'span', {'class': 'toctext'}).get_text(strip=True))
    return lis


def search_results(soup):
    search_results = soup.find("ul", {"class": "mw-search-results"})
    return search_results


def contact(soup):
    keyword = "impressum|kontakt|about us|contact"
    element = soup.find(lambda tag: tag.name == "a" and any(
        kw in (tag.get("href") or tag.text.lower()) for kw in keyword.split("|")))
    print("sheesh")
    if element:
        if element.get("href"):
            contact_form_url = element.get("href")
            print("Kontaktformular-URL gefunden:", contact_form_url)
            return contact_form_url
        else:
            contact_form_url = None
            if "onclick" in element.attrs:
                onclick_value = element.attrs["onclick"]
                print("URL im onclick-Attribut gefunden:", onclick_value)
                return onclick_value

            elif element.text:
                print("URL im Textinhalt gefunden:", element.text)
                return element.text
    else:
        print("Kein Kontaktformular gefunden.")

def hyperlink(soup):
    result = []
    for link in soup.find_all('a'):
        result.append(link.get('href'))
    return result



# trys to find corresponding text and return it. Element must be string
def all_text_2(soup):
    result = []
    for tag in soup.find_all(text=True):
        # Strips annnoying return etc. also removes spaces inbetween the text
        result.append(' '.join(tag.text.strip().replace('\n', '').replace('\r', ' ').split()))
    return result

def all_text(soup):
    return soup.get_text()

def all_text_min_length(soup):
    result = []
    for tag in soup.find_all(text=True):
        # Strips annnoying return etc. also removes spaces inbetween the text
        if len(tag.text.strip().split()) > 5:
            result.append(' '.join(tag.text.strip().replace('\n', '').replace('\r', ' ').split()))
            print(tag.text.strip())
    return result

def convert_output_to_string(output):
    result = '\n'.join(output)
    
    return result


def find_text(soup, text):
    result = []
    for tag in soup.find_all(text=True):
        if text in tag:
            # Strips annnoying return etc. also removes spaces inbetween the text
            result.append(' '.join(tag.text.strip().replace('\n', '').replace('\r', ' ').split()))
    return result


def find_text_metrics(soup, text):
    result = []
    text_counter = 0
    word_counter = 0
    total_words = 0
    total_key_hit = 0
    total_key_hit_near = 0 
    for tag in soup.find_all(text=True):
        if text.lower() in tag.lower():
            word_count = 0
            text_counter += 1
            # Strips annnoying return etc. also removes spaces inbetween the text
            keyword_hits = tag.text.strip().count(text)
            keyword_hits_near = tag.text.strip().count(text.lower())
            word_count += len(tag.text.strip().split())
            total_words += word_count
            total_key_hit += keyword_hits
            total_key_hit_near += keyword_hits_near
            texts = {
                "text": ' '.join(tag.text.strip().replace('\n', '').replace('\r', ' ').split()),
                "length": len(' '.join(tag.text.strip().replace('\n', '').replace('\r', ' ').split())),
                "words": word_count,
                "keyword_exact": keyword_hits,
                "keyword_near": keyword_hits_near
            }
            result.append(texts)
    metrics={
        "all_words": total_words,
        "all_keyword_hits":total_key_hit,
        "all_near_keyword_hits":total_key_hit_near,
    }
    result.insert(0,metrics)
    return result


def find_class(soup, item):
    result = []
    for tag in soup.find_all(class_=re.compile(item)):
        print(tag)
        # Strips annnoying return etc. also removes spaces inbetween the text
        result.append(tag.get_text(strip=True))
    return result

# NEEDS adjustment doesent work always like intendet


def find_id(soup, item):
    result = []
    for tag in soup.find_all(id_=re.compile(item)):
        print(tag)
        # Strips annnoying return etc. also removes spaces inbetween the text
        result.append()
    return result


def find_element(soup, item, element):
    result = []

    for tag in soup.find_all(element):
        if item in tag[element]:
            # Strips annnoying return etc. also removes spaces inbetween the text
            result.append(' '.join(tag.text.strip().replace(
                '\n', '').replace('\r', ' ').split()))
    return result



def analyse_keywords(soup, keyword):
    result = []
    text_counter = 0
    word_counter = 0
    total_words = 0
    total_key_hit = 0
    total_key_hit_near = 0 
    for tag in soup.find_all(text=True):
        if keyword.lower() in tag.lower():
            word_count = 0
            text_counter += 1
            # Strips annnoying return etc. also removes spaces inbetween the text
            keyword_hits = tag.text.strip().count(keyword)
            keyword_hits_near = tag.text.strip().count(keyword.lower())
            word_count += len(tag.text.strip().split())
            total_words += word_count
            total_key_hit += keyword_hits
            total_key_hit_near += keyword_hits_near
            texts = {
                "text": ' '.join(tag.text.strip().replace('\n', '').replace('\r', ' ').split()),
                "length": len(' '.join(tag.text.strip().replace('\n', '').replace('\r', ' ').split())),
                "words": word_count,
                "keyword_exact": keyword_hits,
                "keyword_near": keyword_hits_near
            }
            result.append(texts)
    metrics={
        "all_words": total_words,
        "all_keyword_hits":total_key_hit,
        "all_near_keyword_hits":total_key_hit_near,
    }
    
    result.insert(0,metrics)
    
    return result
# Returns text in one string
def concatenate_texts(result):
    texts_combined = ""
    for item in result[1:]:  # Starte bei Index 1, um die Metriken zu überspringen
        text = item["text"]
        texts_combined += text + " "
    return texts_combined.strip()

def get_date():
    return str(datetime.date.today()).strip()

##!!


def heading_h2_with_text_name_image_auto(soup):
    counter_toc_data = 0
    toc_data = table_of_contents_level_1(soup)
    end_number = len(toc_data) - 1
    content = soup.find('div', {'id': 'content'})

    headings = []
    paragraphs = []

    while counter_toc_data < end_number:
        start = content.find('span', {'class': 'mw-headline'})
        if start:
            print(start, counter_toc_data)
            ueberschrift = start.text.strip()
            headings.append(ueberschrift)
            end = start.find_next_sibling('span', {'class': 'mw-headline'})
            print(end)
            next_element = start.find_next()
            print(ueberschrift)
            if end == None:
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
                        paragraphs.append(
                            "<image-src>"+next_element["src"].strip())
                    if next_element and 'thumbcaption' in next_element.attrs.get('class', []):
                        # if 'magnify' not in next_element.attrs.get('class', []):
                        paragraphs.append(
                            "<image-alt>" + next_element.text.strip())
                    if next_element and next_element.name == 'p':
                        paragraphs.append("<p>"+next_element.text.strip())
                    next_element = next_element.find_next()
        counter_toc_data += 1
    return paragraphs
##!!
