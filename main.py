import urllib.request
import threading
from bs4 import BeautifulSoup as soup
from datetime import datetime
import pandas as pd
import numpy as np
import time
import os
import glob
from app import urls #file storing the urls to webscrape
from IPython.core.display import display,HTML


'''def serverstart(PORT):
    import http.server
    import socketserver

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
'''

def path_to_image_html(main_url, item_link, path, size):
    return '<a href="%s"><img src="%s" width="%d"></a>' % (main_url + item_link, main_url + path, size)


def main():
    #t1 = threading.Thread(target=serverstart, args=(8080,))
    #t1.start()



        #time.sleep(86400)

    oldprice_array = np.array([])
    specialprice_array = np.array([])
    itemname_array = np.array([])
    itemphoto_element_array = np.array([])
    storename_array = np.array([])
    df = pd.DataFrame()
    item_reduction_array = np.array([])

    main_url = "https://www.barkerandstonehouseclearance.co.uk"

    for url in urls.urls:
        headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        page_html = response.read()
        page_soup = soup(page_html, "html.parser")

        for item in page_soup.find_all('div', class_= "col-xs-6 col-md-3 push-center search-item",):
            
            storename_temp = page_soup.title
            storename_temp = storename_temp.get_text().replace(' Furniture Store - Barker & Stonehouse', '')
            
            itemname_element_temp = item.find('span', style="font-weight: bold;text-transform: none!important; font-size: 16px")
            itemname_element_temp = itemname_element_temp.get_text()
            
            specialprice_element_temp = item.find('span', style="color:#ed1b24;font-family:GothamBold21010; font-size:18px;").contents[0]
            specialprice_element_temp = specialprice_element_temp.get_text().strip('£')
            #specialprice_element_temp = int(specialprice_element_temp)

            item_link = item.find('a')['href']

            try:
                specialprice_element_temp = int(specialprice_element_temp)
            except ValueError:
                print("NaN")
                specialprice_element_temp = oldprice_element_temp
            
            oldprice_element_temp = item.find('span', style="text-decoration: line-through; color: #aaa").contents[0]
            oldprice_element_temp = oldprice_element_temp.get_text().strip('£')
            #oldprice_element_temp - int(oldprice_element_temp)

            try:
                oldprice_element_temp = int(oldprice_element_temp)
                if oldprice_element_temp == 0:
                    oldprice_element_temp = 100
            except ValueError:
                print("NaN")
                oldprice_element_temp = 100
                
            

            item_reduction = specialprice_element_temp / oldprice_element_temp

            itemphoto_elements = item.find('img')
            itemphoto_element_temp = itemphoto_elements['data-src']
            itemphoto_element_temp = path_to_image_html(main_url, item_link, itemphoto_element_temp, 120)


            #Appending operations
            storename_array = np.append(storename_array, storename_temp)
            itemname_array = np.append(itemname_array, itemname_element_temp)     
            specialprice_array = np.append(specialprice_array, specialprice_element_temp)
            oldprice_array = np.append(oldprice_array, oldprice_element_temp)
            itemphoto_element_array = np.append(itemphoto_element_array, itemphoto_element_temp)
            item_reduction_array = np.append(item_reduction_array, (1-item_reduction)*100)


    #dataarray = pd.concat([storename_array, itemname_array, specialprice_array, oldprice_array])

    #list_of_files = glob.glob('./*.pkl')  # * means all if need specific format then *.pkl
    #latest_file = max(list_of_files, key=os.path.getctime)
    #prev_df = pd.read_pickle(latest_file)

    df['store'] = storename_array.tolist()
    df['productitemname'] = itemname_array.tolist()
    df['oldpricearray'] = oldprice_array.tolist()
    df['specialpricearray'] = specialprice_array.tolist()
    df['productitemlink'] = itemphoto_element_array.tolist()
    df['itemreduction'] = item_reduction_array.round(1).tolist()
    df['itemreduction'] = df['itemreduction'].astype(str) + '%'
    df['indexcolumn'] = df['store'] + df['productitemname']
    df = df.rename(columns={'store': 'Store', 'productitemname': 'Item Name', 'oldpricearray': 'Original Price', 'specialpricearray' : 'Reduced Price', 'itemreduction' : 'Item Reduction' , 'productitemlink' : 'Item Photo'})


    df = df.set_index('indexcolumn')
    #df.to_pickle('barkerstonehousedf' + datetime.now().strftime('%Y%m%d')+'.pkl')
    df.sort_values(by='Item Reduction', ascending=True)

    a = df.to_html(escape=False, columns = ['Store', 'Item Name', 'Original Price', 'Reduced Price', 'Item Reduction' , 'Item Photo'],
                    col_space=120, index=False, show_dimensions=False, bold_rows=True, classes=["table table-striped table-bordered table-hover table-sm table-dark data-filter-control"], table_id='main_table' )

    return a
'''
    a= HTML(df.to_html(escape=False, columns = ['Store', 'Item Name', 'Original Price', 'Reduced Price', 'Item Reduction' , 'Item Photo'],
                    col_space=120, index=False, show_dimensions=False, bold_rows=True, classes=["table table-striped table-bordered table-hover table-sm table-dark data-filter-control"], table_id='main_table' ))
    html = a.data
'''    

    #boostrap_link = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">'
    #bootstrap_link_2 = '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script> \n<script src="./js/my.js"></script>\n'
    #bootstrap_link_3 = '<div class="container" data-bs-theme="dark"> \n <input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for items.." title="Type in a name"> \n </div> \n'

    #with open('templates/index.html', 'w') as f:
    #    f.write(html)
    #display(HTML(df.to_html(escape=False)))

    #text_file = open("templates/index.html", "w")
    #text_file.write( boostrap_link + '\n' + bootstrap_link_2  + bootstrap_link_3 + html)
    #text_file.close() 




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

