from django.contrib import admin
from .models import Korisnik, BuyProduct, Products, Deposit
from django.core.exceptions import ValidationError
from .forms import MyForm, SetDepositForm, CreateUserForm, BuyProductForm

class MyModel(admin.ModelAdmin):
    form = CreateUserForm
    def get_form(self, request, obj=None, *args, **kwargs):
        form = super(MyModel, self).get_form(request, *args, **kwargs)
        if obj is None:
            form.base_fields["deposit"].disabled = True
        return form


# form to insert current user and to rise validation error if user has role buyer
class UserInitForm(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user_product = request.user

        obj.user_product.save()
        super(UserInitForm, self).save_model(request, obj, form, change)
    # form = MyForm
    # def get_form(self, request, obj=None, *args, **kwargs):
    #     form = super(UserInitForm, self).get_form(request, *args, **kwargs)
    #     form.base_fields['user_product'].initial = request.user
    #     return form

class SetNewDeposit(admin.ModelAdmin):

    form = SetDepositForm

    def get_form(self, request, obj=None, change=False, *args, **kwargs):
        form = super(SetNewDeposit, self).get_form(request, *args, **kwargs)
        form.base_fields['user_deposit'].initial = request.user
        return form

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user_deposit = request.user

        obj.user_deposit.save()
        super(SetNewDeposit, self).save_model(request, obj, form, change)

class NewBuyProduct(admin.ModelAdmin):
    form = BuyProductForm

    def get_form(self, request, obj=None, change=False, *args, **kwargs):
        form = super(NewBuyProduct, self).get_form(request, *args, **kwargs)
        form.base_fields['user_buy'].initial = request.user
        return form

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user_buy = request.user

        obj.user_buy.save()
        super(NewBuyProduct, self).save_model(request, obj, form, change)

class ResetDepositModel(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.buyer = request.user

        obj.buyer.save()
        super(ResetDepositModel, self).save_model(request, obj, form, change)




admin.site.register(Korisnik, MyModel)
admin.site.register(BuyProduct, NewBuyProduct)
admin.site.register(Products, UserInitForm)
admin.site.register(Deposit, SetNewDeposit)
