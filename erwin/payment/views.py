from django.shortcuts import render
from . models import ShippingAddress , Order,OrderItem

from cart.cart import Cart

from django.http import JsonResponse
# Create your views here.


def checkout(request):

    #User with accounts -- Pre - fill the form with user details
    if request.user.is_authenticated:
        try:
            #Authenticated user has a shipping address
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {
                'shipping': shipping_address
            }
            return render(request, 'payment/checkout.html',context=context)
        except :
            #Authenticated user does not have a shipping address
            return render(request, 'payment/checkout.html')
    #Guest user -- Show empty form
    return render(request, 'payment/checkout.html')


def payment_success(request):
    #Clear shopping cart
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]

    return render(request, 'payment/payment-success.html')

def payment_failed(request):
    return render(request, 'payment/payment-failed.html')

def complete_order(request):
    if request.POST.get('action') == 'POST':
        
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')

        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
    
        #All in one shipping address
        shipping_address = (address1 + "\n" + address2 + "\n" + city + "\n" + state + "\n" + zip_code)
        
        #shopping cart information
        cart = Cart(request)


        #Get the total price of items
        total_cost = cart.get_total()

        '''
        Order variations
        1) Create order -> Account users WITH + WITHOUT shipping informations

        2) Create order -> Guest users without an account

        '''


        #1) Create order -> Account users WITH + WITHOUT shipping informations
        if request.user.is_authenticated:
            order = Order.objects.create(full_name = name,email = email,shipping_address = shipping_address,
                                         amount_paid = total_cost, user = request.user
                                         )
            order_id = order.pk

            for item in cart:

                OrderItem.objects.create(order_id = order_id,product=item['product'],quantity=item['qty'],
                                         price = item['price'],user = request.user)
                
        #2) Create order -> Guest users without an account
        else:
            order = Order.objects.create(full_name = name,email = email,shipping_address = shipping_address,
                                        amount_paid = total_cost
                                        )
            order_id = order.pk

            for item in cart:

                OrderItem.objects.create(order_id = order_id,product=item['product'],quantity=item['qty'],
                                        price = item['price'])
                
        order_success = True 
        respose = JsonResponse({'success' : order_success})

        return respose
                
        



    


