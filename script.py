from bs4 import BeautifulSoup
import datetime
from random import shuffle
import requests

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(html, category):
    
    stamp = {}
    
    try:
        sku = html.select('td')[0].get_text().strip()
        stamp['sku'] = sku
    except Exception as e: 
        print(e)
        pass
        
    try:
        sg = html.select('td')[1].get_text().strip()
        stamp['sg'] = sg
    except: 
        stamp['sg'] = None        

    try:
        raw_text = html.select('td')[2].get_text().strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None 
    
    try:
        price = html.select('td')[4].get_text().strip()
        stamp['price'] = price
    except:
        stamp['price'] = None  
        
    stamp['currency'] = "GBP"

    # image_urls should be a list
    images = []                    
    try:
        img_cont = html.select('td')[3]
        img = img_cont.select('a')[0].get('href')
        images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
    
    stamp['category'] = category 
        
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    print(stamp)
    print('+++++++++++++')
           
    return stamp

def get_page_items(url):
    
    items = []
    next_url = ''
    category = ''

    try:
        html = get_html(url)
    except:
        return items, next_url, category
    
    try:
        category_cont = html.find_all('table', attrs={'width':'976'})[0]
        category = category_cont.select('h1')[0].get_text().strip()
    except: 
        pass

    try:
        table_cont = html.find_all('table', attrs={'width':'500'})[0]
        if table_cont:
            for item in table_cont.select('tr'):
                item_width = int(item.select('td')[0].get('width'))
                if (item not in items) and (len(item.select('td')) > 6) and (item_width == 60):
                    items.append(item)
    except:
        pass
    
    try:
        next_cont = html.find_all('p', attrs={'align':'right'})[0]
        next_url_href = next_cont.select('a')[0].get('href')
        if next_url_href != '#':
            url_parts = url.split('/')
            next_url = url.replace(url_parts[-1], next_url_href)
    except:
        pass
    
    shuffle(list(set(items)))
    
    return items, next_url, category

def get_categories():
    
    url = 'http://www.africastamps.co.uk/'
    
    items = []

    try:
        html = get_html(url)

    except:
        return items

    try:
        for item in html.select('table table td > a'):
            item_link = item.get('href')
            item_parts = item_link.split('/')
            if (item_link not in items) and (len(item_parts) == 6): 
                items.append(item_link)
    except: 
        pass
    
    shuffle(list(set(items)))
    
    return items

categories = get_categories()
for category in categories:
    while(category):
        page_items, category, category_name = get_page_items(category)
        for page_item in page_items:
            stamp = get_details(page_item, category_name)

