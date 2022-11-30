from django.urls import include, path

from . import views

urlpatterns = [
    path('seller/', views.sellerlogin, name='sellerlogin'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('manageproduct/',views.manageproduct, name='manageproduct'),
    path('editproduct/<int:pid>',views.editproduct,name='editproduct'),
    path('deleteproduct/<int:pid>',views.deleteproduct,name='deleteproduct'),
    path('sellerindex/',views.sellerindex,name='sellerindex'),


]


