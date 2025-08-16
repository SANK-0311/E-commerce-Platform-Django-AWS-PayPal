from decimal import Decimal
from store.models import Product


class Cart():
    def __init__(self,request):
        self.session = request.session

        #Returning user - obtain their existing session
        cart = self.session.get('session_key')

        #New user - generate a new session

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}


        self.cart = cart


    def add(self, product, product_qty=1):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty

        else:
            self.cart[product_id] = {'qty': product_qty, 'price': str(product.price)}
        
        self.session.modified = True


    def delete(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True


    def update(self, product, qty):
        """
        Update the quantity of a product in the cart.
        """
        product_id = str(product)
        product_quantity = qty
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_quantity
        self.session.modified = True

    def __len__(self):
        """
        Return the total number of items in the cart.
        """
        return sum(item['qty'] for item in self.cart.values())
    
    def __iter__(self):
        """
        Iterate over the items in the cart.
        """

        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        import copy 
        cart = copy.deepcopy(self.cart)
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item
    

    def get_total(self):
        """
        Calculate the total price of the cart.
        """
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())