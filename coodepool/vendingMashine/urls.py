from django.urls import path
from . import views

app_name = 'vendingMashine'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('add-product/', views.addNewProduct, name='add-product'),
    path('user-products/', views.getUserProducts, name='user-products'),
    path('user-products-update/<int:pk>/', views.updateForm, name='user-products-update'),
    path('user-products-delete/<int:pk>/', views.deleteProduct, name='user-products-delete'),
    path('set-deposit/', views.setNewDeposit, name='set-deposit'),
    path('withdraw-deposit/<int:pk>/', views.withdrawDEposit, name='withdraw-deposit'),
    path('all-products/', views.allProducts, name='all-products'),
    path('get-products-data/<int:pk>', views.insertProductForm, name='get-products-data'),
    path('buy-product/<int:pk>', views.buyProducts, name='buy-product'),
    path('all-purchases/', views.allPurchases, name='all-purchases'),
    path('all-products-xhr/', views.showAllProducts, name='all-products-xhr'),
    path('registration/', views.registration, name='registration'),

]