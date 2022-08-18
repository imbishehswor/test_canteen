from django.urls  import path
from . import views

urlpatterns = [
    path('add_to_cart',views.add_to_cart),
    path('coformOrder',views.coformOrder),
    path('multipleOrder',views.multipleOrder),
    path('finalQRcode/<int:id>',views.finalQRcode),
    path('cancelOrder',views.cancelOrder,name="cancelOrder"),
    path('editCart/<int:id>',views.editCart),
    path('deleteItemCart/<int:id>',views.deleteItemCart),
    path('finalCartEdit/<int:id>',views.finalCartEdit),

]
