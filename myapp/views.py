import random

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render

from myapp.models import *
from sellerapp.models import Product
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

 # authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    


def index(request):
    try:
        user_data = User.objects.get(Email=request.session['email'])
        productlist = Product.objects.all()
        return render(request, 'index.html', {'plist': productlist, 'user_data': user_data})
    except:
        productlist = Product.objects.all()
        return render(request, 'index.html', {'plist': productlist})


def shop(request):
    return render(request, 'shop.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        passw = request.POST['password']
        upper = lower = number = special = len1 = False
        if len(passw) >= 8:
            len1 = True
            for i in passw:
                if i.isupper():
                    upper = True
                if i.islower():
                    lower = True
                if i.isdigit():
                    number = True
                if i in '!@#$%^&*':
                    special = True
        if upper and lower and number and special and len1:
            if request.POST['password'] == request.POST['re_password']:
                global user_data
                user_data = {
                    'first_name': request.POST['first_name'],
                    'last_name': request.POST['last_name'],
                    'email_name': request.POST['email'],
                    'mobile_number': request.POST['mobile_number'],
                    'password': request.POST['password'],
                    'r_password': request.POST['re_password'],
                }
                global cotp
                cotp = random.randint(100_000, 999_999)
                subject = 'Account Registration'
                message = f'Hello {user_data["first_name"]}!! \nYour OTP is {cotp}.'
                send_mail(subject, message, settings.EMAIL_HOST_USER,
                        [user_data['email_name']])
                return render(request, 'otp.html')
            else:
                return render(request, 'register.html',{'msg': 'Both passwords do not match!!'} )
        else:
            return render(request, 'register.html', {'msg': 'A combination of uppercase letters, lowercase letters, numbers, and symbols.'})


def otp(request):
    if request.method == 'POST':
        if cotp == int(request.POST['u_otp']):
            global user_data
            user_data = user_data
            User.objects.create(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                Email=user_data['email_name'],
                mobile_number=user_data['mobile_number'],
                password=user_data['password'],
            )
            try:
                global product_add_w_l
               # local_variable = global_variable's_value
                product_add_w_l = product_add_w_l  # variable= value
                # jo aapne koi
                # varialble ne globle define kariae to interpriter same function ma
                # find kare locally so aapne aene locally pan define karvu pade.
                Cart.objects.create(
                    product=Product.objects.get(id=product_add_w_l),
                    quantity=1,
                    user=User.objects.get(Email=user_data['email_name'])
                )
                del product_add_w_l
                del user_data
                return redirect('index')
                # return render(request, 'register.html', {'msg': 'Successfully registered!!'})
            except:
                return redirect('index')

        else:
            return render(request, 'otp.html', {'msg': 'invalid OTP'})
    else:
        return redirect('index')


def login(request):
    if request.method == 'POST':
        try:
            User.objects.get(Email=request.POST['email'])
            request.session['email'] = request.POST['email']
            try:
                global product_add_w_l
                product_add_w_l = product_add_w_l
                Cart.objects.create(
                    product=Product.objects.get(id=product_add_w_l),
                    quantity=1,
                    user=User.objects.get(Email=request.session['email'])
                )
                del product_add_w_l
                return redirect('index')
            except:
                return redirect('index')
        except:
            return render(request, 'login.html', {'msg': 'User Not Found'})
    else:
        return render(request, 'login.html')


def logout(request):
    try:
        request.session['email']
        del request.session['email']
        return redirect('index')
    except:
        return redirect('index')


def addtocart(request, pk):
    try:
        session_user = User.objects.get(Email=request.session['email'])
        Cart.objects.create(
            product=Product.objects.get(id=pk),
            quantity=1,
            user=User.objects.get(Email=request.session['email'])
        )
        return redirect('index')
    except:
        global product_add_w_l
        product_add_w_l = pk
        return render(request, 'login.html')


def cart(request):
    try:
        userobj = User.objects.get(Email=request.session['email'])
        cartdata = Cart.objects.filter(user=userobj)
        
        global final_total
        final_total = actual_price = 0
        for i in cartdata:
            actual_price += i.product.price

        for i in cartdata:
            final_total += i.product.discounted_price
        
        saved_money = actual_price - final_total

        return render(request, 'cart.html', {'plist': cartdata, 'Total': final_total, 'actual_price': actual_price, 'saved_money': saved_money, 'user_data': userobj})
    except:
        return render(request, 'login.html')




def delcart(request, pk):
    cart_object = Cart.objects.get(id=pk)
    cart_object.delete()
    return redirect('cart')



def checkout(request):
    if request.method=='GET':
        currency = 'INR'
        global amount
        amount =  final_total * 100 # Rs. 200
    
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
    
        return render(request,'checkout.html', context=context)

    
    
    # we need to csrf_exempt this url as
    # POST request will be made by Razorpay
    # and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            # result = razorpay_client.utility.verify_payment_signature(
            #     params_dict)
            # if result is not None:
            global amount
            amount = amount # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)

                # render success page on successful caputre of payment
                return render(request, 'paymentsuccess.html')
            except:

                # if there is an error while capturing payment.
                return render(request, 'paymentfail.html')
    # else:

        #     # if signature verification fails.
        #     return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
    # if other than POST request is made.
        return HttpResponseBadRequest()