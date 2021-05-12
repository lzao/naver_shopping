from module.Database import Database
from module.Error import Error
from module.models.NaverShoppingMallModel import NaverShoppingMallModel
from datetime import *
import traceback


class NaverShoppingModel(Database):
    def __init__(self):
        super().__init__()
        self.__error = Error()
        self.__naver_shopping_mall = NaverShoppingMallModel()

    # noinspection PyMethodMayBeStatic
    def store_crawling_products(self, crawling_products):
        try:
            # db 에 저장된 판매처 리스트를 가져옵니다
            mall_list = self.__naver_shopping_mall.get_mall_list()
            quires = []
            for product in crawling_products:
                # 판매처 고유키를 가져옵니다
                mall = [mall_list for mall_list in mall_list if mall_list['mall_name'] == product['mall_name']]
                mall_id = mall[0]['id']
                if not mall:
                    mall_id = self.__store_mall()
                crawling_date = "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())
                sql = "INSERT INTO naver_shopping " \
                      "(`product_name`, `product_price`, `mall_id`, `mall_link`, `crawling_date`) " \
                      "values ('%s', %s, %s, '%s', '%s')" % (product['product_name'],
                                                             product['product_price'],
                                                             mall_id,
                                                             product['mall_link'],
                                                             crawling_date)
                quires.append(sql)
            super().multi_execute(quires)

        except Exception as e:
            print(e)
            error = traceback.format_exc()
            self.__error(error)

    # 크롤링한 판매처가 db 에 저장되어 있지 않으면 db에 저장 후 저장된 고유키 값을 반환합니다
    def __store_mall(self, mall_name):
        sql = "INSERT INTO naver_shopping_mall SET mall_name = '%s'" % mall_name
        super().execute(sql)
        return super().get_insert_id()
