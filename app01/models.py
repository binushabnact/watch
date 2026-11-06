from django.db import models

class register(models.Model):
    contact_firstname = models.CharField(max_length=255)
    contact_lastname = models.CharField(max_length=255)
    contact_Phone = models.IntegerField()
    contact_Email = models.EmailField(max_length=255)
    contact_Uer= models.CharField(max_length=255)
    contact_Password = models.CharField(max_length=255)
    def __str__(self):
     return self.contact_firstname
# Create your models here.

class addprt(models.Model):
    pro_name = models.CharField(max_length=220)
    pro_price = models.FloatField()
    pro_image = models.FileField(null=True,upload_to="products")

    def __str__(self):
       return self.pro_name

class Cart(models.Model):
    cart_user=models.CharField(max_length=250,default=None)
    cart_proid=models.IntegerField(null=True)
    cart_name = models.CharField(max_length=230)
    cart_price = models.FloatField(max_length=290)
    cart_image = models.FileField(null=True)
    cart_qty = models.IntegerField()
    cart_amount = models.FloatField()

    def __str__(self):
        return self.cart_name

class Order(models.Model):
    order_user = models.CharField(max_length=280,default=None)
    order_name = models.CharField(max_length=389)
    order_price = models.FloatField(max_length=320)
    order_image = models.FileField(max_length=250)
    order_qty = models.IntegerField()
    order_amount = models.FloatField()
    order_address = models.TextField(null=True)
    order_paytype = models.CharField(null=True,max_length=10)
    order_status = models.IntegerField(default=0)

    def __str__(self):
        return self.order_name
