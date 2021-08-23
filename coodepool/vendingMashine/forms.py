from django import forms
from .models import Products, Korisnik, Deposit, BuyProduct
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model







class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'role', 'deposit']
        # exclude = ['is_active']


    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['deposit'].widget.attrs['readonly'] = True


class MyForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = '__all__'
        widgets = {'user_product': forms.HiddenInput()}

    def clean(self):
        username = self.cleaned_data['user_product']
        amount = self.cleaned_data['amountAvailable']
        cost = self.cleaned_data['cost']
        prductName = self.cleaned_data['productName']
        user = Korisnik.objects.get(username=username.username)

        if user.role == 'buyer':
            raise ValidationError('You can not enter new products as buyer role')
        if amount < 0:
            raise ValidationError("Entered product's amount is less than 0")
        if cost < 0:
            raise ValidationError("Entered product's cost is less than 0")
        if prductName == None:
            raise ValidationError("Entered fild for product name is empty")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MyForm, self).__init__(*args, **kwargs)
        # self.fields['user_product'].widget = HiddenInput()

class SetDepositForm(forms.ModelForm):

    class Meta:
        model = Deposit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SetDepositForm, self).__init__(*args, **kwargs)


class BuyProductForm(forms.ModelForm):
    class Meta:
        model = BuyProduct
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BuyProductForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data['user_buy']
        formProduct = self.cleaned_data['product_name']
        amountForm = self.cleaned_data['amount']
        user = Korisnik.objects.get(username=username.username)
        product = Products.objects.get(id=formProduct.pk)
        amount = product.amountAvailable - amountForm
        wholePrice = product.cost * amountForm
        checkBuyerDeposite = username.deposit
        if checkBuyerDeposite < wholePrice:
            raise ValidationError('You do not have enough money on your deposit to buy this product.')
        print(amount)
        if product.amountAvailable < amountForm:
            raise ValidationError('You entered product amount to buy higher than amount available')
        if amountForm < 0:
            raise ValidationError('You entered product amount to buy less than zero')
        if user.role == 'seller':
            raise ValidationError('You can not buy products as seller role')


# update product form
class ProductsUpdateForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = '__all__'
        exclude = ['user_product']
        widgets = {
                   'cost': forms.TextInput(attrs={'id':'cost', 'name': 'newcost'}),
                   'amountAvailable': forms.TextInput(attrs={'id':'amount', 'name':'amount'}),
                   'productName': forms.TextInput(attrs={'id':'name', 'name':'name'})}



class BuyProductFormData(forms.ModelForm):
    class Meta:
        model = BuyProduct
        fields = '__all__'
        exclude = ['user_buy', 'product_name']
























