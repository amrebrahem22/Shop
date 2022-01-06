from decimal import Decimal 
from store.models import Product

class Basket:
    """
    A base basket class, providing some default behaviors that can be inherited or overrided as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')

        if 'skey' not in request.session:
            basket = self.session['skey'] = {}

        self.basket = basket

    def add(self, product, product_qty):
        """
        Adding and updating users basket session
        """
        product_id =str(product.id)

        if product_id not in self.basket:
            self.basket[product.id]['qty'] = product_qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': int(product_qty)}

        self.save()

    def __iter__(self):
        """
        Collect product ids in the session data to query the database and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """
        get the basket items count
        """

        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        """
        get the final price
        """
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)
        
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product, product_qty):
        """
        update item from session data
        """
        product_id = str(product)
        
        if product_id in self.basket:
            self.basket[product_id]['qty'] = product_qty
            self.save()

    def save(self):
        self.session.modified = True