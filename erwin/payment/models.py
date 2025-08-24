from django.db import models

from django.contrib.auth.models import User

from store.models import Product


# Create your models here.
class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
 
    #FK #null and black is for optional field
    #Authenticated / not authenticated users
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Shipping Addresses'

    def __str__(self):
        return 'Shipping Address - ' + str(self.id)
    


    
class Order(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15)
    shipping_address = models.TextField(max_length=10000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    date_ordered = models.DateTimeField(auto_now_add=True)

    #FK
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Order - #' + str(self.id)
    


    
class OrderItem(models.Model):
    # FK ->

    order = models.ForeignKey(Order, on_delete=models.CASCADE,null = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null = True)



    quantity = models.PositiveBigIntegerField(default = 1)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    #FK
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Order Item  - #' + str(self.id)
