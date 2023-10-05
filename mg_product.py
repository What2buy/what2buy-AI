from bs4 import BeautifulSoup
import requests

def MgProducts(mg_search_url):
    #step1 : Download the webpage
    url= mg_search_url
    print(url)
    response = requests.get(url)
    html_content = response.text

    #step2 : Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    mg_list = soup.find_all('li', class_='listItem')
    mg_urls = []
    # Limit the loop to the first 5 items
    for unit in mg_list[5:35]:
        # Get product URL
        mg_url = unit.find('div', class_='articleInfo').a.get('href')
        mg_urls.append(mg_url)

    result = True
    mg_clothes = []
    #step1 : Download the webpage
    for i in range(len(mg_urls)):
        url = mg_urls[i]
        response = requests.get(url)
        html_content = response.text

        #step2 : Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        #step3 : 관련상품 url 가져오기
        goods_units = soup.find_all('li', class_='goods-unit')

        if goods_units:  # Check if the list is not empty
            unit = goods_units[0]  # Get the first product

            # Get goods number
            goods_no = unit.get('goods_no')

            # Get product brand
            product_brand = unit.find('a', class_='brand').get_text()

            info = unit.find('a', class_='name')

            # Get product name
            product_name = info.get_text()

            # Get product URL
            product_url = info.get('href')

            # Get image URL
            img_url = unit.find('img').get('data-src')
            # img_url = get_imgUrl(product_url)

            # Get product price
            price = unit.find('span', class_='price').get_text()

            info = {
                "no": goods_no,
                "name": product_name,
                "brand": product_brand,
                "price" : price,
                "img": img_url,
                "url" : product_url,
            }
            mg_clothes.append(info)

    if len(mg_clothes)==0:
        result = False

    return {"result": result, "clothes": mg_clothes}