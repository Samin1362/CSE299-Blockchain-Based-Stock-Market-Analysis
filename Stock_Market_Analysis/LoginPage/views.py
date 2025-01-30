from django.shortcuts import render, redirect
from django.views import View
from .models import LoginPage
from django.contrib.auth.models import User #Importing this user of signup 
from django.contrib import messages #Importing messages. 
from django.contrib.auth import authenticate, login, logout #for authentication of the user. 
from django.db.utils import IntegrityError
from django.conf import settings
from django.core.mail import send_mail
from web3 import Web3
from django.http import HttpResponseRedirect

from .info import w3, chain_id, my_address, private_key, dse 






def login(request, *args, **kwargs):
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'login':
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(username = username, password = password)

            if user is not None: 
                url = "homepage/?output={}".format(username)
                return HttpResponseRedirect(url)
            else:
                messages.error(request, 'Use Correct Credentials')
                return redirect('login')
            
        elif action == 'signup':
            return redirect('signup')
    return render(request, 'login.html', {})
     
def signup(request):
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'signup':
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            if pass1 == pass2:
                username = request.POST['username']
                fname = request.POST['fname']
                lname = request.POST['lname']
                email = request.POST['email']
                address = request.POST['address']
                print(address)
                
                try:
                    user = User.objects.create_user(username, email, pass1)
                    user.first_name = fname
                    user.last_name = lname

                    user.save()

                    modelSave = LoginPage.objects.create(username=username, fname=fname, lname=lname, email=email, address=address, pass1=pass1, pass2=pass2)
                    modelSave.save()

                    messages.success(request, "Your account has been created.")

                    # For welcome email

                    subject = "Welcome to Stock Market Project Login"
                    message = "Hello " + user.first_name + "!! \n" + "Welcome to our project \n" + "Thank you for visiting our website \n We have also sent you a confirmation email, please confirm your email address. \n\n Thanking you\n From our team"
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [user.email]
                    print(to_list)
                    send_mail(subject, message, from_email, to_list, fail_silently=False)

                    return redirect('login')  # Redirect to the login page after successful signup
                
                except IntegrityError:
                    messages.error(request, "Username already exists")
                    return render(request, 'signup.html', {})  # Render the signup page with an error message
            else:
                messages.error(request, 'Password and Confirm Password did not match')
                return redirect('signup')  # Render the signup page with an error message
            

        elif action == 'signin':
            return redirect('login')  # Redirect to the login page if the user clicked on "Sign In" button

    # Handle the case when the request method is not POST or when action is not 'signup' or 'signin'
    return render(request, 'signup.html', {})



#Using a button on homepage to send Email to the client showing them their etherium balance. 
# def homepage(request):

#     if request.method == "POST": 
#         action = request.POST.get('action')
#         if action == 'Check':

#             infura_url = "https://sepolia.infura.io/v3/c64616644cad48f4b28644c74872f1ad"
#             web3 = Web3(Web3.HTTPProvider(infura_url))
#             check_connection = web3.is_connected()
#             if check_connection == True:
#                 balance = web3.eth.get_balance("0x9B79AF9bb193c295Dd63227cDFc59E091eDAcAeB")
#                 subject = "Your Eth Balace"
#                 message = "The banance is " + str(balance)
#                 from_mail = settings.EMAIL_HOST_USER

#                 send_mail(subject, message, from_mail, ['saminisrak1991@gmail.com'], fail_silently=False)
                
#                 return redirect('home')

#             return redirect('home')
#         return

#     return render(request, "home.html", {})

def homepage(request):

    username = request.GET.get('output')

    nonce = w3.eth.get_transaction_count(my_address)

    store_transaction = dse.functions.registerUser(username).build_transaction(
        {
            "chainId":chain_id,
            "gasPrice":w3.eth.gas_price,
            "from":my_address,
            "nonce":nonce,
        }
    )
    sign_store_transaction = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
    send_transaction = w3.eth.send_raw_transaction(sign_store_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_transaction)

    see = dse.functions.users(my_address).call()


    return render(request, 'Navbar.html', {'username':username})

#For transaction Page
def transaction(request):

    username = request.GET.get('output')

    if request.method == 'POST':

        transaction_type = request.POST.get('transaction_type')
        
        if transaction_type == "buy":
            stock_id = request.POST.get('stock_id')
            quantity = request.POST.get('quantity')

            nonce = w3.eth.get_transaction_count(my_address)
            print(nonce)

            store_transaction = dse.functions.buyStock(int(stock_id), int(quantity)).build_transaction(
                {
                    "chainId": chain_id,
                    "gasPrice": w3.eth.gas_price,  # Use the higher gas price
                    "from": my_address,
                    "nonce": nonce,
                }
            )
            sign_store_transaction = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
            send_transaction = w3.eth.send_raw_transaction(sign_store_transaction.rawTransaction)
            transaction_receipt = w3.eth.wait_for_transaction_receipt(send_transaction)

            return render(request, 'transaction.html', {})
        
        elif transaction_type == 'sell':
            
            stock_id = request.POST.get('stock_id')
            quantity = request.POST.get('quantity')

            nonce = w3.eth.get_transaction_count(my_address)
            print(nonce)

            store_transaction = dse.functions.sellStock(int(stock_id), int(quantity)).build_transaction(
                {
                    "chainId": chain_id,
                    "gasPrice": w3.eth.gas_price,  # Use the higher gas price
                    "from": my_address,
                    "nonce": nonce,
                }
            )
            sign_store_transaction = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
            send_transaction = w3.eth.send_raw_transaction(sign_store_transaction.rawTransaction)
            transaction_receipt = w3.eth.wait_for_transaction_receipt(send_transaction)

            return render(request, 'transaction.html', {})


        return render(request, 'transaction.html', {})

    return render(request, 'transaction.html', {})


def stock(request):

    stocks_list = []

    i = 1
    while i <= 4:
        see = dse.functions.stocks(i).call()
        stock_data = {
            'id': see[0],
            'name': see[1],
            'price': see[2],
            'available_quantity': see[3]
        }
        stocks_list.append(stock_data)
        i += 1

    owned_stocks = []

    see = dse.functions.getStocksOwnedDetails(my_address).call()

    for stock in see:
        owned_stock_info = {
            'id': stock[0],
            'name': stock[1],
            'price': stock[2],
            'quantity': stock[3]
        }
        owned_stocks.append(owned_stock_info)

    context = {
        'stocks': stocks_list,  # Pass the list of stocks in the context
        'owned_stocks': owned_stocks  # Pass the list of owned stocks in the context
    }

    return render(request, 'stock.html', context)

def account(request):
    username_ = request.GET.get('output')

    user = LoginPage.objects.get(username=username_)

    balance = dse.functions.users(my_address).call()

    context = {
        'client':user,
        'balance':balance[2],
    }

    return render(request, 'account.html', context)

def test(request):
    return render(request, 'test.html', {})