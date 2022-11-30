from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('logout/', views.logout, name="logout"),
    path('cart/',views.cart,name='cart'),
    path('shop/',views.shop,name='shop'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('otp/',views.otp,name='otp'),
    path('addtocart/<int:pk>',views.addtocart,name='addtocart'),
    path('delcart/<int:pk>', views.delcart, name="delcart"),
    path('checkout/',views.checkout,name='checkout'),
    path('checkout/paymenthandler/',views.paymenthandler,name='paymenthandler'),
]


