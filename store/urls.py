from django.urls import path
from . import views
urlpatterns = [
    path('',views.store, name="store"),
    path('checkout/',views.checkout, name="checkout"),
    path('cart/',views.cart, name="cart"),
    path('update_item/',views.UpdateItem, name="update_item"),
    path('process_order/',views.ProcessOrder, name="process_order"),
    path('user_logout/',views.userLogout, name = "user_logout"),
    path('login_register/', views.loginOrRegister,name="login_register"),
    #path('tiffin/<int:tid>', views.tiffin, name="tiffin"),
    path('vendor/<int:vid>', views.vendor, name="vendor"),
    path('my_orders/', views.myOrders, name="myOrders"),

]
