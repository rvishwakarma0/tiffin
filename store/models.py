from django.db import models
from django.contrib.auth.models import User

Rating = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True,unique=True)

    

    def __str__(self):
        return self.name


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True, unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=200)
    rating = models.CharField(
        max_length=1,
        choices=Rating,
        default='3'
    )
    description = models.CharField(max_length=500, null=True, blank=True)
    photo1 = models.ImageField(null= True, blank=True)
    photo2 = models.ImageField(null=True, blank=True)
    photo3 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def getPhoto1(self):
        try:
            url = self.photo1.url
        except:
            url = ''
        return url

    @property
    def getPhoto2(self):
        try:
            url = self.photo2.url
        except:
            url = ''
        return url

    @property
    def getPhoto3(self):
        try:
            url = self.photo3.url
        except:
            url = ''
        return url

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=True, null=True, blank=False)
    image = models.ImageField(null=True, blank = True)
    rating = models.CharField(
        max_length=1,
        choices=Rating,
        default='3'
    )
    description = models.CharField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total    

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


