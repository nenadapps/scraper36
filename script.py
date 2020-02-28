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
    except:
        pass
    
    
    sg = None
    item_value = None
    if(len(html.select('td')) > 4):
        raw_text_index = 3 
        price_index = 5
        image_index = 4 
        try:
            sg = html.select('td')[1].get_text().strip()
        except: 
            pass
        
        try:
            item_value = html.select('td')[2].get_text().strip()
        except: 
            pass
    else:
        raw_text_index = 1 
        price_index = 3 
        image_index = 2 
    
    stamp['sg'] = sg
    stamp['item'] = item_value
        
    try:
        raw_text = html.select('td')[raw_text_index].get_text().strip()
        stamp['raw_text'] = raw_text.replace('"',"'")
    except:
        stamp['raw_text'] = None 
    
    try:
        price = html.select('td')[price_index].get_text().strip()
        stamp['price'] = price
    except:
        stamp['price'] = None  
        
    stamp['currency'] = "GBP"

    # image_urls should be a list
    images = []                    
    try:
        img_cont = html.select('td')[image_index]
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
                td0 = item.select('td')[0].get_text().strip()
                if (item not in items) and (len(item.select('td')) > 3) and ((item_width == 60) or (item_width == 55)) and (td0 !='Item ID'):
                    items.append(item)
    except:
        pass
    
    try:
        next_cont = html.find_all('p', attrs={'align':'right'})[0]
        next_url_href = next_cont.select('a')[0].get('href')
        next_url_text = next_cont.get_text().strip()
        if (next_url_href != '#') and ('Top of Page' not in next_url_text) and ('Back to Top' not in next_url_text):
            url_parts = url.split('/')
            next_url = url.replace(url_parts[-1], next_url_href)
    except:
        pass
    
    shuffle(list(set(items)))
    
    return items, next_url, category

def get_categories():
    
    url = 'http://www.africastamps.co.uk/singleitems.html'
    
    items = []

    try:
        html = get_html(url)

    except:
        return items

    try:
        for item in html.select('table table td a'):
            item_href = item.get('href')
            item_link = 'http://www.africastamps.co.uk/' + item_href
            item_parts = item_href.split('/')
            if (item_link not in items) and (len(item_parts) == 3): 
                print(item_link)
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

