from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('index', views.index, name="index"),
    path('wholesales', views.wholesales, name="wholesales"),
    path('retail', views.retail, name="retail"),
    path('subs-main', views.subsMain, name="subsmain"),
    path('subs/<str:subname>', views.subs, name="subs"),
    path('stock-quantity', views.stockQuantity, name="stockquantity"),
    path('confirmation', views.confirmation, name="confirmation"),
    path('admin-panel', views.adminPanel, name="adminpanel"),
    path('settings', views.settings, name="settings"),
    path('delivery-shop', views.deliveryShop, name="deliveryshop"),
    path('delivery', views.delivery, name="delivery"),
    path('invoice', views.invoice, name="invoice"),
    path('error', views.showerror, name="error"),
    path('emergency/register', views.register, name="register"),
]