from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from coodepool import settings





class MyKorisnikManager(BaseUserManager):
    def create_user(self, username, password=None):

        if not username:
            raise ValueError('Morate unjeti username')


        user = self.model(
            username=username,

        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Korisnik(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='datum pristupanja', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='poslednje prijavljivanje', auto_now=True)
    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    ROLE = [
        ('seller','seller'),
        ('buyer', 'buyer')
    ]
    role = models.CharField(max_length=256, choices=ROLE)
    deposit = models.IntegerField(null=True, blank=True, default=0,)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = MyKorisnikManager()

    def __str__(self):
        return self.username + ' --- ' + self.role + ' --- ' + f'Deposit: {self.deposit} coins'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Products(models.Model):
    user_product = models.ForeignKey(Korisnik, on_delete=models.CASCADE, help_text='User is entered by authentication')
    amountAvailable = models.IntegerField(null=True, blank=True, default=0, verbose_name='Amount available', help_text="Enter product's amount")
    cost = models.IntegerField(null=True, blank=True, default=0, help_text="Enter product's cost value")
    productName = models.CharField(blank=True, null=True, max_length=256, verbose_name='Product name', help_text="Enter product's name")

    def __str__(self):
        return str(self.productName) + ' ---------- ' + 'Amount available: ' + str(self.amountAvailable)




class Deposit(models.Model):
    user_deposit = models.ForeignKey(Korisnik, on_delete=models.CASCADE, related_name='buyer')
    DEPOSIT = [
        (5, '5'),
        (10, '10'),
        (20, '20'),
        (50, '50'),
        (100, '100'),
    ]
    add_deposit = models.IntegerField(null=True, blank=True, default=0, choices=DEPOSIT)

    def __str__(self):
        return self.user_deposit.username + ' ' + f'deposit: {str(self.add_deposit)}'

    def save(self, *args, **kwargs):
        user = Korisnik.objects.get(id=self.user_deposit.pk)
        print(user.deposit)
        user.deposit = user.deposit + self.add_deposit
        user.save()
        super(Deposit, self).save(*args, **kwargs)


class BuyProduct(models.Model):

    product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_buy = models.ForeignKey(Korisnik, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, blank=True, default=0)
    cost = models.IntegerField(null=True, blank=True, default=0)


    def __str__(self):
        return f"{self.user_buy.username} buy {self.amount} of {self.product_name.productName}"







