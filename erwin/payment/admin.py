from django.contrib import admin


from .models import ShippingAddress,Order,OrderItem
admin.site.register(ShippingAddress)

admin.site.register(Order)
admin.site.register(OrderItem)












# Register your models here.
# admin.site.site_header = 'Erwin Admin'
# admin.site.site_title = 'Erwin Admin Portal'
# admin.site.index_title = 'Welcome to Erwin Admin Portal' 

