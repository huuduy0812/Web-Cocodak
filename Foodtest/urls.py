"""Foodtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static
from user import views as account_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='index'),
    path('dishdetail/<int:id>', views.dishdetail_view, name='dishdetail'),
    path('order/', views.order_view, name='order'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', account_view.SiteLoginView, name='login'),
    path('profile/', account_view.SiteProfilesView.as_view(), name='profile'),
    path('register/', account_view.SiteRegisterView, name='register'),
    path('register/access/', account_view.register_access, name='register_access'),
    path('logout/', account_view.SiteLogoutView.as_view(), name='logout'),
    path('changepassword/', account_view.ChangePasswordSite, name='change_password'),
    path('addcart/', views.addcart, name='addcart'),
    path('search/', views.search_view, name='search'),
    path('deletecart/', views.deletecart, name='deletecart'),
    path('activate/<uidb64>/<token>', account_view.activate, name='activate'),
    path('forgotPassword/', account_view.forgotPassword, name='forgotPassword'),
    path('forgotPassword/access', account_view.forgotPassword_access, name='forgotPassword_access'),
    path('reset_password_validate/<uidb64>/<token>', account_view.reset_password_validate, name='reset_password_validate'),
    path('reset_password', account_view.reset_password, name='reset_password'),
    path('quantity_cart/', views.quantity_cart, name='quantity_cart'),
    path('favorite/', views.Favorite_view, name='favorite'),
    path('favorite_status/', views.favorite, name='favorite_status'),
    path('deletecart_index/', views.deletecart_index, name='deletecart_index'),
    path('orderdetail/', views.orderdetail, name='orderdetail'),
    path('ordernow/', views.ordernow, name='ordernow'),
    path('addorder/', views.addorder, name='addorder'),
    path('checkout/', views.checkout, name='checkout'),
    path('deletefavorite/', views.deletefavorite, name='deletefavorite'),
    path('checkout_process/', views.checkout_process, name='checkout_process'),
    path('ordernow_process/', views.ordernow_process, name='ordernow_process'),
    path('checkout_ordernow_process/', views.checkout_ordernow_process, name='checkout_ordernow_process'),
    path('favorite_add_check/', views.favorite_add_check, name='favorite_add_check')

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
