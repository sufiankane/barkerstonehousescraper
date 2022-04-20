import urllib.request
import logging
import threading
from bs4 import BeautifulSoup as soup
from datetime import datetime
import pandas as pd
import numpy as np
import time
import os
import glob
from IPython.core.display import display,HTML

def serverstart(PORT):
    import http.server
    import socketserver

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def path_to_image_html(path):
    return '<img src="'+ path + '" width="120" >'

def main():
    t1 = threading.Thread(target=serverstart, args=(8080,))
    t1.start()

    urls: list[str] = [
    'https://www.barkerandstonehouse.co.uk/clearance/store-clearance/darlington-clearance?product_list_limit=all',
    'https://www.barkerandstonehouse.co.uk/clearance/store-clearance/guildford-clearance?product_list_limit=all',
    'https://www.barkerandstonehouse.co.uk/clearance/store-clearance/hove-clearance?product_list_limit=all',
    'https://www.barkerandstonehouse.co.uk/clearance/store-clearance/hull-clearance?product_list_limit=all',
    'https://www.barkerandstonehouse.co.uk/clearance/store-clearance/knaresborough-clearance?product_list_limit=all',
    'https://www.barkerandstonehouse.co.uk/clearance/store-clearance/leeds-clearance?product_list_limit=all',
    'https://www.barkerandstonehouse.co.uk/clearance/store-clearance/london-battersea-clearance?product_list_limit=all',
    'https://www.barkerandstonehouse.co.uk/clearance/store-clearance/metro-retail-park-clearance?product_list_limit=all',
    'https://www.barkerandstonehouse.co.uk/clearance/store-clearance/newcastle-clearance?product_list_limit=all',
    'https://www.barkerandstonehouse.co.uk/clearance/store-clearance/nottingham-clearance?product_list_limit=all',
    'https://www.barkerandstonehouse.co.uk/clearance/store-clearance/teesside-park-clearance?product_list_limit=all',
    ]

    oldpricearray = np.array([])
    specialpricearray = np.array([])
    productitemname = np.array([])
    productitemlink = np.array([])
    productitemphoto = np.array([])
    storename = np.array([])

    for url in urls:
        headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        page_html = response.read()
        #time.sleep(0.5)
        page_soup = soup(page_html, "html.parser")

        if len(page_soup.find_all('span', class_= "old-price",)) ==\
            len(page_soup.find_all('span', class_= "special-price",)) ==\
            len(page_soup.find_all('a', class_= "product-item-link",)) ==\
            len(page_soup.find_all('a', class_= "product-item-link", href=True)) ==\
            len(page_soup.find_all('img', class_= "product-image-photo")):

            for price in page_soup.find_all('div', class_= "clearance-store-header__title",):
                storenametemp = price.get_text('')

            for price in page_soup.find_all('span', class_= "old-price",):
                #print(price.get_text('').strip('Was £'))
                oldpricearray = np.append(oldpricearray, price.get_text('').strip('Was £'))
                storename = np.append(storename, storenametemp)

            for price in page_soup.find_all('span', class_= "special-price",):
                #print(price.get_text('').strip('Now £'))
                specialpricearray = np.append(specialpricearray, price.get_text('').strip('Now £'))

            for price in page_soup.find_all('a', class_= "product-item-link",):
                #print(price.get_text(''))
                productitemname = np.append(productitemname, price.get_text(''))

            for price in page_soup.find_all('a', class_= "product-item-link", href=True):
                #print(price['href'])
                productitemlink = np.append(productitemlink, price['href'])

            for price in page_soup.find_all('img', class_= "product-image-photo"):
                #print(path_to_image_html(price['src']))
                productitemphoto = np.append(productitemphoto, path_to_image_html(price['src']))


        else:
            print('Mismatch at ' + url)

    print(storename.shape, productitemname.shape, oldpricearray.shape, specialpricearray.shape, productitemphoto.shape, productitemlink.shape)
    #print(page_soup.prettify())

    #dataarray =  pd.concat[storename, productitemname, oldpricearray, specialpricearray, productitemphoto, productitemlink]

    #list_of_files = glob.glob('C:/Users/Hamnah/PycharmProjects/pythonProject/*.pkl')  # * means all if need specific format then *.pkl
    list_of_files = glob.glob('./*.pkl')  # * means all if need specific format then *.pkl
    latest_file = max(list_of_files, key=os.path.getctime)
    prev_df = pd.read_pickle(latest_file)

    df = pd.DataFrame()
    df['store'] = storename.tolist()
    df['productitemname'] = productitemname.tolist()
    df['oldpricearray'] = oldpricearray.tolist()
    df['specialpricearray'] = specialpricearray.tolist()
    df['productitemphoto'] = productitemphoto.tolist()
    df['productitemlink'] = productitemlink.tolist()
    df['indexcolumn'] = df['store'] + df['productitemname']

    df = df.set_index('indexcolumn')
    df.to_pickle('barkerstonehousedf' + datetime.now().strftime('%Y%m%d')+'.pkl')

    df_sofa = df[df['productitemname'].str.contains('sofa') | df['productitemname'].str.contains('Sofa')]
    df_chest = df[df['productitemname'].str.contains('chest') | df['productitemname'].str.contains('Chest')]

    df_compare_whatsnew = df.ne(prev_df)
    #df_compare_whatsnew = df_compare_whatsnew.filter(like='False', axis=0)
    df_compare_whatsgone = prev_df.ne(df)
    #df_compare_whatsgone = df_compare_whatsgone.filter(like='False', axis=0)

    a= HTML(df.to_html(escape=False))
    html = a.data
    with open('barkerstonehouse' + datetime.now().strftime('%Y%m%d') + '.html', 'w') as f:
        f.write(html)
    display(HTML(df.to_html(escape=False)))

    a= HTML(df.to_html(escape=False))
    html = a.data
    with open('index.html', 'w') as f:
        f.write(html)
    display(HTML(df.to_html(escape=False)))

    a= HTML(df_compare_whatsnew.to_html(escape=False))
    html = a.data
    with open('whatsnewbarkerstonehouse' + datetime.now().strftime('%Y%m%d') + '.html', 'w') as f:
        f.write(html)
    display(HTML(df_compare_whatsnew.to_html(escape=False)))

    a= HTML(df_compare_whatsgone.to_html(escape=False))
    html = a.data
    with open('whatsgonebarkerstonehouse' + datetime.now().strftime('%Y%m%d') + '.html', 'w') as f:
        f.write(html)
    display(HTML(df_compare_whatsgone.to_html(escape=False)))

    a= HTML(df_chest.to_html(escape=False))
    html = a.data
    with open('chestbarkerstonehouse' + datetime.now().strftime('%Y%m%d') + '.html', 'w') as f:
        f.write(html)
    display(HTML(df_chest.to_html(escape=False)))

    a= HTML(df_sofa.to_html(escape=False))
    html = a.data
    with open('sofabarkerstonehouse' + datetime.now().strftime('%Y%m%d') + '.html', 'w') as f:
        f.write(html)
    display(HTML(df_sofa.to_html(escape=False)))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

