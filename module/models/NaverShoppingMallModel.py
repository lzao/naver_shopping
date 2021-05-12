from module.Database import Database


class NaverShoppingMallModel(Database):
    __mall_list = []

    def __init__(self):
        super().__init__()

    def get_mall_list(cls):
        if not cls.__mall_list:
            sql = "SELECT * FROM naver_shopping_mall"
            return super().execute(sql)
        else:
            return cls.__mall_list
