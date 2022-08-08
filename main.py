import re
import requests
from lxml import html


def extract_from_link(link, my_file):
    global count
    images = []

    data = requests.get(link).content
    source_code = html.fromstring(data)

    x_path = "//*[@id='MainContent_ListView1_Image2_"

    for i in range(9):
        try:
            img_path = x_path + str(i) + "']"
            images.append(source_code.xpath(img_path)[0].attrib['src'])
        except:
            break

    title = source_code.xpath('//*[@id="MainContent_lbl_Product_Name"]')[0].text_content()
    price = source_code.xpath('//*[@id="MainContent_LbL_salesPrice"]')[0].text_content()
    id = source_code.xpath('//*[@id="MainContent_lbl_ProID"]')[0].text_content()
    description = source_code.xpath('//*[@id="collapse1-1"]/div/div[1]')[0].text_content()
    brand = source_code.xpath('//*[@id="MainContent_HyperLink1_Brand"]')[0].text_content()

    meta_text = f"<%-- Pro${count}  --%>\n\n"
    meta_text += f'<meta property="og:title" content="{title}" />\n'
    meta_text += f'<meta property="og:type" content="xxxxxxxxxxxxxx" />\n'
    for img in images:
        meta_text += f'<meta property="og:url" content="{img}" />\n'
    meta_text += f'<meta property="og:price:amount" content="{price}">\n'
    meta_text += f'<meta property="og:price:currency" content="GBP">\n'
    meta_text += f'<meta property="og:availability" content="in stock">\n'
    meta_text += f'<meta property="og:description" content="{description}">\n'
    meta_text += f'<meta property="product:retailer_item_id" content="{id}">\n'
    meta_text += f'<meta property="product:condition" content="new">\n'
    meta_text += f'<meta property="product:brand" content="{brand}">\n\n\n'
    my_file.write(meta_text)


file = open("ewp_links.txt", "r+")
links = file.read().splitlines()
file.close()

file = open("meta_props.txt", "w+", encoding="utf-8")
count = 0
for lin in links:
    count += 1
    extract_from_link(lin, file)
    print(str(count)+" from "+str(len(links)))

file.close()
