"""ecommtradingapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from rest_framework import urls

from .import views
from .views import ProductApi, ConsumptionApi, ProductProvider, AnnouncemetAPI, CartItemViews, productAdd
from rest_framework.routers import DefaultRouter

from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

    #path('admin/', admin.site.urls),

    #path('questions/', views.QuestionsAPIView.as_view()),
    path('consumption',views.consumption,name='consumption'),
    path(r'displaydata',views.tUserApi,name = 'displaydata'),
    path('signup',views.userregistration),
    path('login',views.login, name = 'login'),
    path('addProductProvider',views.addProductProvider, name = 'addProductProvider'),
    path('logout',views.logout,name = 'logout'),
    path('reporting',views.reporting,name = 'reporting'),
    #path('individualConsumption',views.individualConsumption,name = 'individualConsumption'),
    path(r'api/t_user', views.t_userApi),


    path(r'api/t_user/update', CartItemViews.as_view()),
    path(r'api/t_user/update/<int:id>', CartItemViews.as_view()),

    path(r'api/productProvider', views.t_product_providerApi),
    path(r'api/productProvider', ProductProvider.as_view()),
    path(r'api/productProvider/<int:id>', ProductProvider.as_view()),
    #path('productProvider',views.productProvider),
    #path('showemp',views.showEmp),
    path('rat/<int:id>',views.rat),
    path('productCancel/<int:id>',views.productCancel),

    path(r'api/products', views.t_productsApi),
    path(r'api/products', ProductApi.as_view()),
    path(r'api/products/<int:id>', ProductApi.as_view()),
    path('addProduct',views.productAdd),

    path(r'api/consumption', views.t_consumptionsApi),
    path(r'api/consumption', ConsumptionApi.as_view()),
    path(r'api/consumption/<int:id>', ConsumptionApi.as_view()),

    #path('search',views.tablesjoin),

    path(r'api/announcements', views.t_announcementsApi),
    path(r'api/announcements', AnnouncemetAPI.as_view()),
    path(r'api/announcements/<int:id>', AnnouncemetAPI.as_view()),

]

