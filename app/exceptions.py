class ProductNotFound(Exception):
    pass

class ProductAlreadyExist(Exception):
    def __init__(self, product_name: str):
        self.product_name = product_name