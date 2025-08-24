from django.urls import path

from . import views



urlpatterns = [
    #path('payment/', views.register, name='payement'),
    path('payment_success/', views.payment_success, name='payment-success'),
    path('payment_failed/', views.payment_failed, name='payment-failed'),
    path('checkout/', views.checkout, name='checkout'),
    path('complete-order',views.complete_order,name='complete-order'),
]
