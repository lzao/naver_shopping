import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from module.models.NaverShoppingModel import NaverShoppingModel
from module.Error import Error
import time
import re
import constant
import traceback


class Crawling(object):

    def __init__(self):
        self.__limit = int(constant.CRAWLING_LIMIT)
        self.__query = constant.CRAWLING_QUERY
        self.__link = "https://search.shopping.naver.com/search/all?" \
                      "origQuery=desimone&pagingIndex=%d&pagingSize=%d&productSet=total&query=%s"

        self.__options = Options()
        # gui 환경이 아닌 곳에서 사용하기 위해 headless option을 추가합니다
        self.__options.add_argument("--headless")
        self.__driver = None

        self.__error = Error()

    def crawling(self):
        try:
            # 크롤링할 사이트의 페이지네이션 값입니다
            next_page = 1
            while True:
                self.__driver = webdriver.Firefox(firefox_options=self.__options,
                                                  executable_path=constant.ROOT_PATH + '/' + constant.DRIVER_FILE)
                # 크롤링할 사이트의 url link를 가져옵니다
                link = self.__get_crawl_link(next_page)
                self.__driver.get(link)
                # 크롤링할 사이트의 해당 페이지에 있는 상품 개수를 가져옵니다
                product_count = self.__get_product_count()
                # 상품 개수가 없다면 크롤링을 끝냅니다
                if product_count == 0:
                    self.__driver.quit()
                    break

                # 크롤링할 상품 정보 리스트를 가져옵니다
                product_list = self.__get_data(product_count)
                # 크롤링한 상품 정보 리스트를 DB에 저장합니다
                naver_shopping = NaverShoppingModel()
                naver_shopping.store_crawling_products(product_list)
                # 다음 페이지네이션으로 이동하기 위한 값을 세팅합니다
                next_page = next_page + 1
        except Exception as e:
            print(e)
            error = traceback.format_exc()
            self.__error.logging(error)

    # 검색한 페이지에서 상품이름, 상품가격, 판매처이름을 가져옵니다
    def __get_data(self, product_count):
        try:
            # 상품 리스트의 정보를 담고 있는 element 입니다
            products = self.__driver.find_elements_by_css_selector('ul[class=list_basis] > div > div')

            array_index = 0
            product_list = []
            for productElement in products:
                # 상품카테고리, 상품이름, 상품 가격을 담고 있는 element 입니다
                product = productElement.find_element_by_css_selector("li > div > div:nth-child(2)")
                # 상품 카테고리 중 프로바이오틱스가 아닌 것은 수집하지 않습니다
                product_category = productElement.find_element_by_css_selector("div:nth-child(3) > a:last-child").text
                if product_category != '프로바이오틱스':
                    continue
                # 상품 이름을 가져옵니다
                product_name = product.find_element_by_css_selector("div > a").text
                # 상품 가격을 가져옵니다
                product_price = product.find_element_by_css_selector(
                    "div:nth-child(2) > strong > span > span[class^=price_num__]").text
                # 상품 가격의 숫자를 제외한 문자를 제거합니다
                product_price = re.sub("[^0-9]", "", product_price)

                # 상품 이름, 상품 가격, 판매처 이름을 리스트에 저장합니다
                product_list.append({
                    'product_name': product_name,
                    'product_price': product_price,
                    'mall_name': '',
                    'mall_link': ''
                })

                # 판매처 정보를 가지고 있는 element 입니다
                mall = productElement.find_element_by_css_selector("li > div > div:nth-child(3)")
                # 판매처 링크를 설정합니다
                mall_info = mall.find_element_by_css_selector("div > div[class^=basicList_mall_title__] > a")
                mall_link = mall_info.get_attribute('href')
                product_list[array_index]['mall_link'] = mall_link
                # 판매처 리스트로 표시되는 element 입니다
                mall_lists = mall.find_elements_by_css_selector("div > ul[class^=basicList_mall_list__] > li")
                if len(mall_lists) > 0:
                    for mall_list in mall_lists:
                        mall_info = mall_list.find_element_by_css_selector("span[class^=basicList_mall_name__]")
                        mall_name = mall_info.text
                        product_price = mall_list.find_element_by_css_selector("span[class^=basicList_price]").text
                        product_price = re.sub("[^0-9]", "", product_price)

                        # index 값이 중복이면 데이터를 덮어씌웁니다. 중복되지 않으면 새로 append 합니다
                        if len(product_list) == array_index + 1:
                            product_list[array_index]['product_price'] = product_price
                            product_list[array_index]['mall_name'] = mall_name
                        else:
                            product_list.append({
                                'product_name': product_name,
                                'product_price': product_price,
                                'mall_name': mall_name,
                                'mall_link': mall_link
                            })
                        array_index = array_index + 1
                else:
                    # 판매처 정보가 하나만 나오는 경우를 처리합니다
                    mall_name = mall.find_element_by_css_selector("div > div[class^=basicList_mall_title__] > a").text
                    # 판매처 이름이 이미지 나온 경우를 처리합니다
                    if mall_name == '':
                        mall_name = mall.find_element_by_css_selector(
                            "div > div[class^=basicList_mall_title__] > a > img").get_attribute('alt')
                    # 판매처 이름을 설정합니다
                    product_list[array_index]['mall_name'] = mall_name

                    array_index = array_index + 1
            self.__driver.quit()
            return product_list
        except Exception as e:
            print(e)
            error = traceback.format_exc()
            self.__error.logging(error)

    # 크롤링할 사이트의 url link 를 설정합니다
    def __get_crawl_link(self, add_page_number=1):
        link = self.__link % (add_page_number, self.__limit, self.__query)
        return link

    # 크롤링할 사이트의 해당 페이지에 있는 상품 개수를 가져옵니다
    def __get_product_count(self):
        try:
            last_product_count = 0
            while True:
                # 무한 스크롤일 경우 window.scrollTo를 사용하여 스크롤 다운합니다
                self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # 로딩 하는 속도를 고려하여 sleep 합니다, 컴퓨터가 아닌 것처럼 보이기 위해 랜덤으로 sleep 값을 설정합니다
                time.sleep(random.uniform(0.5, 5))
                products = self.__driver.find_elements_by_css_selector('ul[class=list_basis] > div > div')
                # 상품 리스트의 개수가 중복이 되면 스크롤이 끝났으므로 loop 에서 빠져나옵니다
                if last_product_count == len(products):
                    break
                last_product_count = len(products)

            return last_product_count
        except Exception as e:
            print(e)
            error = traceback.format_exc()
            self.__error.logging(error)
