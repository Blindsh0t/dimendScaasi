from requests_html import HTMLSession
from datetime import date
import csv
import re
import os


# for ease, save scraped file at desktop
os.chdir('/Users/hardikpatel/Desktop')


# timestamp as filename
today = date.today().strftime('%b_%d_%Y')
head = ['Shape', 'Price', 'Size', 'Cut', 'Color', 'Grade', 'certi']


# returns list with page numbers
def pages():
    li = []
    url = 'https://www.dimendscaasi.com/loose-diamonds/?numined_vendor=548&limits=12&pagecount='
    pages_want_to_scrape = 500
    
    for i in range(pages_want_to_scrape):
        url_li = li.append(url + str(i))
    return li


# gets the url and passes to parse it
def get_session():
    url_list = pages()
    session = HTMLSession()
    for each in url_list:
        r = session.get(each)
        parse(r)



# gets the required fields, if they exist
def parse(x):
    dia_box = x.html.find('div.box_bottam_area')
    for each in dia_box:
        tag = str(each.find('a'))
        texts = each.text
        list_form = texts.split('\n')

        price = list_form[1].replace('$','').replace(',','')
        shape = list_form[list_form.index([i for i in list_form if i.startswith('Shape')][0]) + 1]
        carat = list_form[list_form.index([i for i in list_form if i.startswith('Carat')][0]) + 1].replace(' ct.','')
        color = list_form[list_form.index([i for i in list_form if i.startswith('Color')][0]) + 1]
        clarity = list_form[list_form.index([i for i in list_form if i.startswith('Clarity')][0]) + 1]
        try:
            cut = list_form[list_form.index([i for i in list_form if i.startswith('Cut')][0]) + 1]
            certi = re.findall(r'[A-Za-z]+[\d]{3,}', tag)[0]
        except:
            cut = ''
            certi = ''
        data = {
                'Shape': shape, 
                'Price': price, 
                'Size': carat, 
                'Cut': cut, 
                'Color': color, 
                'Grade': clarity, 
                'certi': certi
                }
        writer().writerows([data])



def writer():
    # f_nm = desktop + today
    f = open(today, 'a', newline='')
    csv_writer = csv.DictWriter(f, fieldnames=head)

return csv_writer


def csv_headings():
    writer().writeheader()


def main():
    writer()
    csv_headings()
    pages()
    get_session()


if __name__="__main__":
    main()
