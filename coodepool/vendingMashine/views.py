from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import JsonResponse, HttpResponse





def index(request):

    user = request.user
    context = {}
    try:
        currentUser = Korisnik.objects.get(id=user.pk)
        idCurrentUser = currentUser.pk
        context['currentUser'] = currentUser
        context['idCurrentUser'] = idCurrentUser

        purchasesAll = BuyProduct.objects.filter(user_buy__username=user.username)
        context['purchases'] = purchasesAll
    except Korisnik.DoesNotExist:
        comment = None
    form = MyForm(request.POST or None, initial={'user_product': request.user})
    formUpdate = ProductsUpdateForm(request.POST or None)
    formDeposit = SetDepositForm(request.POST or None, initial={'user_deposit': request.user})

    context['user'] = user
    context['form'] = form
    context['formUpdate'] = formUpdate
    context['formDeposit'] = formDeposit

    return render(request, 'vendingMashine/index.html', context)


def addNewProduct(request):
    form = MyForm(request.POST or None)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        validate = form.save(commit=False)
        name = validate.productName
        user = request.user
        if int(validate.amountAvailable) < 0:
            return JsonResponse({'error':'You entered amount of products less than 0'})
        if Products.objects.filter(productName=name, user_product__username=user.username):
            return JsonResponse({'error': 'You have this item in your shop.'})
        else:
            validate.save()
        return JsonResponse({'message': 'You created new product successfully!'})
    return JsonResponse({'error':'You did not created new product'})


def getUserProducts(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user = request.user
        userData = Korisnik.objects.get(username=user.username)

        username = userData.username
        products = Products.objects.filter(user_product__username=userData.username).values().order_by('productName')
        dictOfProducts = []
        for product in products:
            dictOfProducts.append(product)
        return JsonResponse({'data':dictOfProducts, 'username':username})
    return render(request, 'vendingMashine/copy.html', {})

def updateForm(request, pk=None):

    product = Products.objects.get(id=pk)

    # updateInstance = model_to_dict(product)
    form = ProductsUpdateForm(request.POST or None)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cost = request.POST.get('cost')
        amount = request.POST.get('amount')
        product.amountAvailable = amount
        product.cost = cost
        product.user_product = request.user
        product.save()
        return JsonResponse({'update':'Product has been updated'})

    return JsonResponse({'error': 'Product has not been updated'})

def deleteProduct(request, pk=None):
    product = Products.objects.get(id=pk)
    name = product.productName
    if request.method == 'DELETE':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            product.delete()
            return JsonResponse({'update': f'Product {name} has been deleted'})

    return JsonResponse({'error': 'Product has not been deleted'})

def setNewDeposit(request):
    user = request.user

    form = SetDepositForm(request.POST or None)
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            depo = form.save(commit=False)
            deposit = depo.add_deposit
            depo.save()
            if user:
                userId = Korisnik.objects.get(id=user.pk)
                fullDeposit = userId.deposit
                return JsonResponse({'message': f'You set new deposit {deposit} successfully!', 'newDeposit':fullDeposit})
            else:
                return JsonResponse({'message': f'You set new deposit {deposit} successfully!', 'newDeposit': 0})
    return JsonResponse({'error': 'You did not set deposit'})

def withdrawDEposit(request, pk=None):
    user = Korisnik.objects.get(id=pk)
    if request.method == 'PUT':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            withdraw_deposit = user.deposit
            user.deposit = 0
            user.save()
            from .helper import set_coins

            listOfCoins1 = [5, 10, 20, 50, 100]
            dictOfCoinsAmount = {}
            deposit = withdraw_deposit
            set_coins(deposit, listOfCoins1, dictOfCoinsAmount)
            print(withdraw_deposit)

            return JsonResponse({'message':'Your deposit is 0', 'coins':dictOfCoinsAmount})
    return JsonResponse({'error': 'You did not withdraw deposit'})


def allProducts(request):
    products = Products.objects.all()
    form = BuyProductFormData(request.POST or None)
    context = {
        'products': products,
        'form': form
    }
    user = request.user
    return render(request, 'vendingMashine/buy_products.html', context)

def buyProducts(request, pk=None):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                amount = request.POST.get('amount')

                product = Products.objects.filter(productName__isnull=False)
                for p in product:
                    if p.pk == pk:


                        wholePrice = int(p.cost) * int(amount)
                        pro = Products.objects.get(id=p.pk)
                        proAmount = int(pro.amountAvailable) - int(amount)
                        user = request.user
                        userQuery = Korisnik.objects.get(id=user.pk)
                        userDeposit = userQuery.deposit
                        if int(wholePrice) > int(userDeposit):
                            return JsonResponse({'error': 'You have no enough money on you deposit account to buy this product'})
                        if int(p.amountAvailable) < int(amount):
                            return JsonResponse({'error': 'Requested amount of product is higher than in stock. Please order less amount. '})
                        if userQuery.role == 'seller':
                            return JsonResponse({'error': 'You can not buy items as seller role.'})

                        else:
                            buyProduct = BuyProduct.objects.create(product_name=p, user_buy=request.user, amount=p.cost,
                                                                   cost=wholePrice)
                            buyProduct.save()
                            newDeposit = int(userDeposit) - int(wholePrice)
                            userQuery.deposit = newDeposit
                            userQuery.save()
                            userNew = request.user
                            userQueryNew = Korisnik.objects.get(id=userNew.pk)
                            userDepositNew = userQueryNew.deposit
                            pro.amountAvailable = proAmount
                            pro.save()


                            return JsonResponse({'message': 'You purchase was successfull!', 'newDeposit': userDepositNew, 'productName': p.productName,
                                                 'amountAvailable':proAmount, 'cost':p.cost, 'pk':p.pk})

            except Korisnik.DoesNotExist:
                user = None


    return JsonResponse({'error': 'Some error occured. Try again.'})

def insertProductForm(request, pk=None):
    context = {}
    product = ''
    try:
        user = request.user
        product = Products.objects.filter(productName__isnull=False)
        for p in product:
            if p.pk == pk:
                context['productName'] = p.productName
                context['amountAvailable'] = p.amountAvailable
                context['cost'] = p.cost
                context['pk'] = p.pk
    except Korisnik.DoesNotExist:
        user = None
    print(context)

    return JsonResponse(context)

def allPurchases(request):
    user = request.user
    try:
        user = Korisnik.objects.get(id=user.pk)
        context = {}
        purchasesAll = BuyProduct.objects.filter(user_buy__username=user.username)
        for purch in purchasesAll:
            context['id'] = purch.pk
            context['product_name'] = purch.product_name.productName
            context['user_buy'] = purch.user_buy.username
            context['amount'] = purch.amount

        return JsonResponse(context)


    except Korisnik.DoesNotExist:
        user = None

    return render(request, 'vendingMashine/copy.html', {})

def showAllProducts(request):
    context = {}
    product = Products.objects.all().values('id','user_product__username', 'amountAvailable', 'cost', 'productName')
    counter = 0
    for p in product:
        context[f'product_{counter}'] = [p]
        counter = counter + 1
    return JsonResponse(context)

def registration(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/index/')
    else:
        form = CreateUserForm()

    return render(request, 'vendingMashine/registration_form.html', {'form':form})


from django.contrib.auth.models import User


