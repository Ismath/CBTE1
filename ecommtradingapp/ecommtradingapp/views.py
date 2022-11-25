#import rating as rating
from MySQLdb import connections
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites import requests
from django.db.backends import mysql
from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from django.template import loader
from django.db import connection
# import the modules
from pymysql import*
#import xlwt
import numpy as np
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
import seaborn as sn

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

#@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def rat(request,id):
    if request.method == 'POST':
        try:
            rating1 = request.POST['rating']
            print("rating1##################" + rating1)
            #print("id##################" + id)
            record = t_consumptions.objects.get(id=id)
            # update name
            record.rating = rating1
            record.status = 'Completed'
            record.save()
            return redirect('consumption')
        except Exception as e:
            print(e)

    return render(request,"RatingDetails.html")
def cancelConsumption(request,id):

    try:
        cancel = t_consumptions.objects.get(id=id)
        cancel.status = 'Cancelled'
        cancel.save()
        return redirect('consumption')
    except Exception as e:
        print(e)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def tUserApi(request):

    results = t_products.objects.all()
    #a = t_consumptions.filter()

    if request.method == 'POST':

        #t = (product,user)
        try:
            t = request.POST['product_id']
            user = request.POST['district']

            request.session['product_id'] = t

            cursor = connection.cursor()

            sql =    ("SELECT pr.name,u.uname, pp.district,pp.location,  pp.t_product_provider_id, pr.product_id, c.rating from ecommtradingapp_t_consumptions c, ecommtradingapp_t_product_provider pp, ecommtradingapp_t_user u, ecommtradingapp_t_products pr where c.product_id_id=pr.product_id  and c.product_id_id=pp.product_id_id and c.product_provider_id_id=pp.t_product_provider_id and pp.user_id_id=u.user_id and c.product_id_id = %s and pp.district = %s and c.status ='Completed'")
            data = [t,user]

            cursor.execute(sql,data)
            res = cursor.fetchall()

            print(res);

            sql2 = (
                "SELECT pr.name,u.uname, pp.district,pp.location, pp.t_product_provider_id, pr.product_id from ecommtradingapp_t_product_provider pp, ecommtradingapp_t_user u, ecommtradingapp_t_products pr where pp.product_id_id=pr.product_id  and pp.user_id_id=u.user_id and pp.product_id_id = %s and pp.district = %s")
            #data = [t, user]

            cursor2 = connection.cursor()
            cursor2.execute(sql2, data)
            probs = cursor2.fetchall()

            print(probs);

            solutions=[]
            dfSol = pd.DataFrame()

            # [1] Get the input .csv library and problem cases
            # {pandas.DataFrame}
            df = pd.DataFrame(res)
            df.to_csv('input/library.csv', index=False, header=['Product','Provider','District','Address','Product Provider ID','Product ID','Ratings'])

            df2 = pd.DataFrame(probs)
            df2.to_csv('input/cases.csv', index=False,  header=['Product','Provider','District','Address','Product Provider ID','Product ID'])

            library, cases = pd.read_csv('input/library.csv'), pd.read_csv('input/cases.csv')

            # Print
            print('\n> Initial Library')
            print(f'\n{library}')
            print(f'\n{cases}')

            # Select columns from library to use as base cases, except solutions
            base = library.iloc[:, range(library.shape[1] - 1)]  # Exclude last column (solution)

            # Print
            print('\n> Base')
            print(f'\n{base}')

            # [2] Initial One-hot encoding
            base = pd.get_dummies(base)
            problems = pd.get_dummies(cases)

            # Print
            print('\n> One-hot encoding')
            print(f'\n{base}')
            print(f'\n{problems}\n')

            # [3] Calculate
            # Print
            print('\n> Calculating\n')

            # Move through all problem cases
            for i in range(problems.shape[0]):
                # Print
                print(f'\n{base} for problem {i}')

                # [3.1] Get inverse covariance matrix for the base cases
                covariance_matrix = base.cov()  # Covariance
                inverse_covariance_matrix = np.linalg.pinv(covariance_matrix)  # Inverse

                # [3.2] Get case row to evaluate
                case_row = problems.loc[i, :]

                # Empty distances array to store mahalanobis distances obtained comparing each library cases
                distances = np.zeros(base.shape[0])

                # [3.3] For each base cases rows
                for j in range(base.shape[0]):
                    # Get base case row
                    base_row = base.loc[j, :]

                    # [3.4] Calculate mahalanobis distance between case row and base cases, and store it
                    distances[j] = distance.mahalanobis(case_row, base_row, inverse_covariance_matrix)

                # [3.5] Returns the index (row) of the minimum value in distances calculated
                min_distance_row = np.argmin(distances)

                # [4] Get solution based on index of found minimum distance, and append it to main library
                # From cases, append library 'similar' solution
                case = np.append(cases.iloc[i, :], library.iloc[min_distance_row, -1])

                # Print
                print(f'> For case/problem {i}: {cases.iloc[i, :].to_numpy()}, solution is {case[-1]}')

                # [5] Store
                # Get as operable pandas Series
                case = pd.Series(case, index=library.columns)  # Case with Solution
                dfSol = dfSol.append(case, ignore_index=True)
                library = library.append(case, ignore_index=True)  # Append to library
                # Save 'covariance heat map (biased)' output as file
                sn.heatmap(np.cov(base, bias=True), annot=True, fmt='g')
                plt.gcf().set_size_inches(12, 6)
                plt.title(f'Covariance Heat map #{i} \n Library cases stored {j} - Base to solve problem {i}')
                plt.savefig(f'output/covariance_heat_map_{i}.png', bbox_inches='tight')
                plt.close()

                # [6] Reuse
                base = library.iloc[:, range(library.shape[1] - 1)]  # Exclude last column (solution)
                base = pd.get_dummies(base)  # Get new one-hot encoded base

            # [7] Output
            print('\n> Output library')
            print(f'\n{library}')

            solutions = dfSol.values.tolist()

            # [7] Output
            print('\n> Output solutions')
            print(f'\n{solutions}')


            # Save 'library' output as file
            library.to_csv('output/library.csv', index=False)

            return render(request, "template.html", {'displaydata': solutions})

        except Exception as e:
            print (e)

    return render(request, "search.html", { "t_products": results})

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def addProductProvider(request):

    results = t_products.objects.all()
    #a = t_consumptions.filter()

    if request.method == 'POST':

        #t = (product,user)
        try:

            uname = request.session['uname']
            print(uname)

            x = t_user.objects.get(uname=uname).user_id
            print(x)

            location = request.POST['location']
            district = request.POST['district']
            volunteer = request.POST['volunteer']
            description = request.POST['description']
            long = request.POST['long']
            width = request.POST['width']
            product_id = request.POST['product_id']


            print("djk")

            ins = t_product_provider(location=location, district=district, volunteer=volunteer, description=description, long=long,
                                     width=width, user_id_id=x, product_id_id=product_id)
            ins.save()

            print("save##################")
            return render(request, "ProductProvider.html", {'t_products': results})

        except Exception as e:
            print (e)
    print("end#################33")
    return render(request, "ProductProvider.html", { "t_products": results})

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
        #return render(request=request, template_name="signup.html")
        return redirect('login')
    return render(request=request, template_name="signup.html")


def addConsumption (request, productProviderId, productId) :

    uname = request.session['uname']
    print(uname)

    x = t_user.objects.get(uname = uname) . user_id
    print(x)

    rating = 0
    #product_id = request.session['product_id']
    ins1 = t_consumptions(rating=rating,  user_id_id = x , product_id_id=productId, product_provider_id_id=productProviderId )
    ins1.save()
    print("sucess")
    messages.success(request, "registered successfully")
    return redirect('consumption')
    #displaydata = t_consumptions.objects.filter(user_id_id = x).values('id','product_id_id','status','user_id_id')


    # print(displaydata)
    #
    # template = loader.get_template('Consumption.html')
    # context = {
    #     'mymembers': displaydata,
    #
    #   }
    #
    # return HttpResponse(template.render(context, request))

def consumption (request) :

    uname = request.session['uname']
    print(uname)

    x = t_user.objects.get(uname = uname) . user_id
    print(x)

    rating = 0
    # product_id = request.session['product_id']
    # ins1 = t_consumptions(rating=rating,  user_id_id = x , product_id_id=product_id )
    # ins1.save()
    # print("sucess")
    # messages.success(request, "registered successfully")

    #displaydata = t_consumptions.objects.filter(user_id_id = x).values('id','product_id_id','status','user_id_id')

    cursor = connection.cursor()

    sql = (
        "SELECT pr.name, (select uname from ecommtradingapp_t_user where user_id=pp.user_id_id) as uname, pp.district,pp.location, c.start_time, c.end_time, c.status, c.rating, pp.t_product_provider_id, pr.product_id, c.id from ecommtradingapp_t_consumptions c, ecommtradingapp_t_product_provider pp, ecommtradingapp_t_user u, ecommtradingapp_t_products pr where c.product_id_id=pr.product_id  and c.product_id_id=pp.product_id_id and c.product_provider_id_id=pp.t_product_provider_id and c.user_id_id=u.user_id and u.user_id=%s")
    data = [x]

    cursor.execute(sql, data)
    res = cursor.fetchall()

    print(res);

    print(displaydata)

    template = loader.get_template('Consumption.html')
    context = {
        'mymembers': res,

      }

    return HttpResponse(template.render(context, request))


def login(request):

    if request.method == "POST" :
        try:
            Userdetails = t_user.objects.get(uname = request.POST['uname'],  pwd = request.POST['pwd'])

            request.session['utype'] = Userdetails.utype
            request.session['uname'] =Userdetails.uname

            if request.session['utype'] == 'consumer' :
                print("if$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                return redirect('displaydata')
            else:
                print("else$$$$$$$$$$$$$$$$$$$$$$$$$$")
                return redirect('addProductProvider')

        except Exception as e:

           messages.success(request,'username and password invalid')

    return render(request=request, template_name="login.html")


def index(request):
    return redirect('login')

def logout(request):
    try:
        del request.session['uname']
        del request.session['product_id']
    except:
        return redirect('login')
    return redirect('login')



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
        return render(request=request, template_name="addingProduct.html")
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

def reporting(request):
    #results = t_products.objects.all()
    # a = t_consumptions.filter()

    if request.method == 'POST':
        try:
            import mysql.connector
            import pandas as pd
            s = request.POST['from']
            print (s)
            #date_sr = pd.to_datetime(pd.Series(s))
            #change_format = date_sr.dt.strftime('%y-%m-%d')

            e = request.POST['todate']
            print(e)
            #date_sr1 = pd.to_datetime(pd.Series(e))
            #change_format1 = date_sr1.dt.strftime('%y-%m-%d')

            my_conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="cbte1_trading"
            )
            ####### end of connection ####
            my_data = pd.read_sql(
                " SELECT ecommtradingapp_t_products.name,ecommtradingapp_t_product_provider.location,count(*),ecommtradingapp_t_consumptions.creation_date from ecommtradingapp_t_consumptions inner join ecommtradingapp_t_product_provider on ecommtradingapp_t_consumptions.product_id_id = ecommtradingapp_t_product_provider.product_id_id inner join ecommtradingapp_t_products on ecommtradingapp_t_consumptions.product_id_id = ecommtradingapp_t_products.product_id where ecommtradingapp_t_consumptions.status ='Completed' and ecommtradingapp_t_consumptions.creation_date between %s and %s group by ecommtradingapp_t_product_provider.location and ecommtradingapp_t_consumptions.product_id_id and ecommtradingapp_t_consumptions.creation_date ",
                my_conn,params=[s,e])
            df1 = pd.DataFrame(my_data)
            df1.to_csv(r'C:\Users\LENOVO\Downloads\exported_data.csv',index=False)
            print(my_data)
            #df= (" SELECT ecommtradingapp_t_products.name,ecommtradingapp_t_product_provider.location,count(*) from ecommtradingapp_t_consumptions inner join ecommtradingapp_t_product_provider on ecommtradingapp_t_consumptions.product_id_id = ecommtradingapp_t_product_provider.product_id_id inner join ecommtradingapp_t_products on ecommtradingapp_t_consumptions.product_id_id = ecommtradingapp_t_products.product_id where ecommtradingapp_t_consumptions.product_id_id = %s and ecommtradingapp_t_product_provider.location = %s and ecommtradingapp_t_consumptions.status ='Completed' group by ecommtradingapp_t_product_provider.location ")
            #data = [t, user]
            #cursor.execute(df, data)
            #res = cursor.fetchall()

            return render(request, "template.html")

        except Exception as e:
            print(e)


    return render(request, "reportingModule.html")


