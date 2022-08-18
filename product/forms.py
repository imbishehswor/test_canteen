
from statistics import mode
from tkinter import Widget
# from attr import field
from django import forms

from product.models import Product

# from product.models import Product 
  
class productForm(forms.Form):  #ImagefieldForm
    product_name = forms.CharField() 
    product_photo = forms.ImageField()
    product_desc = forms.CharField(widget=forms.Textarea)
    product_price= forms.IntegerField()
    product_active = forms.BooleanField()
    
    class Meta:
        model = Product
        field = "__all__"

        Widget = {
            'product_name':forms.TextInput(attrs={'class':'field'}),
            'product_price':forms.NumberInput(attrs={'class':'field'}),
            'product_desc':forms.TextInput(attrs={'class':'field'}),
        }

    

    # forms.URLField()