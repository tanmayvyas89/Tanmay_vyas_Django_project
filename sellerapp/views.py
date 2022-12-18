from django.shortcuts import render, redirect, HttpResponse
import sellerapp
from sellerapp.models import *

# Create your views here.


def sellerlogin(request):
    if request.method == 'POST':
        try:
            Seller.objects.get(Email=request.POST['Email'])
            request.session['Email'] = request.POST['Email']
            return redirect('sellerindex')
        except:
            return render(request, 'sellerlogin.html', {'msg': 'User not found'})
    else:
        return render(request, 'sellerlogin.html')


def addproduct(request):
    sellerobj = Seller.objects.get(Email=request.session['Email'])
    if request.method == "POST":
        original_price = int(request.POST['PRICE']) 
        discount = int(request.POST['percentage_discount'])
        discounted_price = original_price - (original_price * (discount / 100))
        Product.objects.create(
            seller=sellerobj,
            product_name=request.POST['product_name'],
            product_description=request.POST['description'],
            price=request.POST['PRICE'],
            quantity=request.POST['available_quantity'],
            discount=request.POST['percentage_discount'],
            discounted_price=discounted_price,
            image=request.FILES['Main_Image'],
            first_name=request.POST['seller_name'],

        )

        return render(request, "sellerindex.html")
    else:
        return render(request, 'addproduct.html')


def manageproduct(request):
    productlist = Product.objects.all()
    return render(request, 'manageproduct.html', {'plist': productlist})


def editproduct(request, pid):
    productobj = Product.objects.get(id=pid)
    if request.method == 'POST':
        if 'pic' in request.FILES:
            productobj.product_name = request.POST['product_name']
            productobj.des = request.POST['description']
            productobj.price = request.POST['PRICE']
            productobj.discount = request.POST['percentage_discount']
            productobj.quantity = request.POST['available_quantity']
            productobj.image = request.FILES['Main_image']
            productobj.save()
            return redirect('manageproduct')
        else:
            productobj.product_name = request.POST['product_name']
            productobj.des = request.POST['description']
            productobj.price = request.POST['PRICE']
            productobj.discount = request.POST['percentage_discount']
            productobj.quantity = request.POST['available_quantity']
            # productobj.image=request.FILES['Main_image']
            productobj.save()
            return redirect('manageproduct')
    return render(request, 'editproduct.html', {'pobj': productobj})


def deleteproduct(request, pid):
    productobj = Product.objects.get(id=pid)
    if request.method == 'POST':
        productobj.delete()
        return redirect('manageproduct')
    return render(request, 'deleteproduct.html', {'pobj': productobj})


def sellerindex(request):
    sellerdetails = Seller.objects.all()
    return render(request, 'sellerindex.html', {'sellerlist': sellerdetails})
