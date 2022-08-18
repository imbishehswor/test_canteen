from turtle import update
from django.urls import path
from . import views

urlpatterns = [
    path('addProducts', views.uploadProduct),
    path('viewProduct',views.showProduct),
    path('editProduct/<int:id>',views.editProduct),
    path('deleteProduct/<int:id>',views.deleteProduct),
    path('updateProduct/<int:id>',views.updateProduct),
    path('dailyUpdate',views.dailyUpdate),
    path('menu',views.menu),
    

    # path('viewProduct',views.showProduct,name='viewProduct'),
    # path('seeEditProduct',views.seeEditProduct),
    # path('productDelete/<int:id>',views.productDelete),
    # path('productEdit/<int:id>',views.productEdit),
    # path('updateProduct/<int:id>',views.updateProduct),
]
