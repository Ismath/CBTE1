import rating as rating
from MySQLdb import connections
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites import requests
from django.db.backends import mysql
from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from django.template import loader
from django.db import connection


from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from django.core import serializers
from .models import t_user, t_announcements, t_consumptions, t_products, t_product_provider, displaydata
from django.views.decorators.csrf import csrf_exempt

from .serializers import T_announcementsSerializer, T_consumptionSerializer, T_productSerializer, \
    T_product_providerSerializer, T_userSerializer, T_consumptionproductProvider
from mysql import connector

def rat(request):
    if request.model == 'POST':
        rating = request.POST('rating')
        try:
            x = request.session['id']
            patient_edit = t_consumptions.objects.get(id=x)  # object to update
            patient_edit.rating = rating  # update name
            patient_edit.save()
            return render(request, "Consumption.html")
        except Exception as e:
            print(e)

    return render(request, "RatingDetails.html")


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def tUserApi(request):

    results = t_products.objects.all()
    #a = t_consumptions.filter()

    if request.method == 'POST':

        #t = (product,user)
        try:
            t = request.POST['product_id']
            user = request.POST['location']

            request.session['product_id'] = t

            cursor = connection.cursor()

            sql =    (" SELECT ecommtradingapp_t_consumptions.product_id_id,ecommtradingapp_t_consumptions.rating,ecommtradingapp_t_product_provider.location from ecommtradingapp_t_consumptions join ecommtradingapp_t_product_provider on ecommtradingapp_t_consumptions.product_id_id = ecommtradingapp_t_product_provider.product_id_id where ecommtradingapp_t_consumptions.product_id_id = %s and ecommtradingapp_t_product_provider.location = %s and ecommtradingapp_t_consumptions.status ='Completed' ")
            data = [t,user]
            cursor.execute(sql,data)
            res = cursor.fetchall()

            return render(request, "template.html", {'displaydata': res})

        except Exception as e:
            print (e)

    return render(request, "search.html", { "t_products": results})

def userregistration(request):
    if request.method == 'POST' :
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        ufullname = request.POST['ufullname']
        uemail = request.POST['uemail']
        udob = request.POST['udob']
        unic = request.POST['unic']
        uaddress = request.POST['uaddress']
        utelephone = request.POST.get('utelephone', False)
        utype = request.POST['utype']

        print("djk")
        ins = t_user(uname = uname , pwd = pwd , ufullname = ufullname ,uemail = uemail, unic = unic,udob=udob, uaddress = uaddress, utelephone = utelephone, utype = utype)
        ins.save()

        messages.success(request,"registered successfully")
        return render(request=request, template_name="signup.html")
    return render(request=request, template_name="signup.html")

def consumption (request) :

    uname = request.session['uname']
    print(uname)

    x = t_user.objects.get(uname = uname) . user_id
    print(x)

    rating = 0
    product_id = request.session['product_id']
    ins1 = t_consumptions(rating=rating,  user_id_id = x , product_id_id=product_id )
    ins1.save()
    print("sucess")
    messages.success(request, "registered successfully")

    displaydata = t_consumptions.objects.filter(user_id_id = x).values('id','product_id_id','status','user_id_id')
    displaydata1 = t_consumptions.objects.filter(id = )
    request.session['id'] = displaydata.id

    print(displaydata)

    template = loader.get_template('Consumption.html')
    context = {
        'mymembers': displaydata,

      }

    return HttpResponse(template.render(context, request))


def login(request):

    if request.method == "POST" :
        try:
            Userdetails = t_user.objects.get(uname = request.POST['uname'],  pwd = request.POST['pwd'])

            request.session['utype'] = Userdetails.utype
            request.session['uname'] =Userdetails.uname

            if request.session['utype'] == 'consumer' :
                return redirect('displaydata')
            else:
                return render(request=request, template_name="ProductProvider.html")

        except Exception as e:
            messages.success(request,'username and password invalid')

    return render(request=request, template_name="login2.html")


def logout(request):
    try:
        del request.session['uname']
        del request.session['product_id']
    except:
        return render(request,'index.html')
    return render(request, 'index.html')



# t_user
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def t_userApi(request, id=0):
    if request.method == 'GET':
        users = t_user.objects.all()
        serializer = T_userSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = T_userSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemViews(APIView):
    def patch(self, request, id=None):
        item = t_user.objects.get(user_id=id)

        serializer = T_userSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():

            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(t_user, user_id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


# t_product_provider

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def t_product_providerApi(request):
    if request.method == 'GET':
        product_provider = t_product_provider.objects.all()
        serializer = T_product_providerSerializer(product_provider, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = T_product_providerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductProvider(APIView):

    def patch(self, request, id=None):

        item = t_product_provider.objects.get(t_product_provider_id=id)

        serializer = T_product_providerSerializer(item, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save()

            return Response({"status": "success", "data": serializer.data})

        else:

            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):

        item = get_object_or_404(t_product_provider, t_product_provider_id=id)

        item.delete()

        return Response({"status": "success", "data": "Item Deleted"})
def AddproductProvider(request):
    
    return render(request=request, template_name="search.html")











@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def t_productsApi(request):
    if request.method == 'GET':
        products = t_products.objects.all()
        serializer = T_productSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = T_productSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductApi(APIView):
    def patch(self, request, id=None):
        item = t_products.objects.get(product_id=id)

        serializer = T_productSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():

            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(t_products, product_id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


def productAdd(request):
    if request.method == 'POST' :
        proname = request.POST['proname']
        prodesc = request.POST['prodesc']

        print("djk")
        ins = t_products(name = proname , description = prodesc  )
        ins.save()

        messages.success(request,"Product added successfully")
        return render(request=request, template_name="signup.html")
    return render(request=request, template_name="addingProduct.html")



# t_consumptions
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def t_consumptionsApi(request):
    if request.method == 'GET':
        consumptions = t_consumptions.objects.all()
        serializer = T_consumptionSerializer(consumptions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = T_consumptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsumptionApi(APIView):
    def patch(self, request, id=None):
        item = t_consumptions.objects.get(product_id=id)

        serializer = T_consumptionSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():

            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(t_consumptions, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


# t_announcements
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def t_announcementsApi(request):
    if request.method == 'GET':
        announcements = t_announcements.objects.all()
        serializer = T_announcementsSerializer(announcements, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = T_announcementsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnnouncemetAPI(APIView):
    def patch(self, request, id=None):
        item = t_announcements.objects.get(id=id)

        serializer = T_announcementsSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():

            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(t_announcements, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


# Create your views here.
def users(request):  # pull data from third party rest api
    response = requests.get('http://127.0.0.1:8080/api/t_user')  # convert reponse data into json
    users = response.json()
    # print(users)
    # return HttpResponse("Users")
    return render(request, "users.html", {'users': users})
    pass

