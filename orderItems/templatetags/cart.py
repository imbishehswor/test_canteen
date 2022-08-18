# from django import template

# register = template.Library()


# @register.filter(name='is_in_cart')
# def is_in_cart(product,cart):
#     # keys = cart.keys()
#     print (product,cart)
#     return True

from django import template
register = template.Library()


@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0 

@register.filter(name='price_total')
def price_total(product, cart):
    
    return product.product_price * int(cart_quantity(product, cart)) 


@register.filter(name='total_final_price')
def total_final_price(products, cart):
    sum = 0
    for p in products:
        sum += price_total(p,cart)

    return sum