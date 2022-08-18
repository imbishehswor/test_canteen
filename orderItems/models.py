from django.db import models
from accounts.models import Users
from product.models import Product
import datetime

# Create your models here.
class Order_items(models.Model):
    # order_id = models.BigAutoField(primary_key=TRUE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    
    class Meta:
        db_table = "order_item"


class Order_details(models.Model):
    # order_product_id = models.BigAutoField(primary_key=TRUE)
    order = models.ForeignKey(Order_items, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    

    class Meta:
        db_table= "order_details"


class Qrcode(models.Model):
    order_id = models.IntegerField()
    user_fullname = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField()
    quantity = models.IntegerField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    class Meta:
        db_table = "qrcode"
    

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = "cart"







    