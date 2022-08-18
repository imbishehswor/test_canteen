from django.db import models

# Create your models here.
class Product(models.Model):
    # product_id = models.BigAutoField(primary_key=True) #models.IntegerField(primary_key=TRUE,auto_now_add=True)
    product_name = models.CharField(max_length=100)
    product_photo = models.ImageField(upload_to = "productPhotos/")
    product_desc = models.TextField(max_length=500,null=True)
    product_price = models.IntegerField()
    product_active = models.BooleanField()
    
    
    class Meta:
        db_table = "product"

    
    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

