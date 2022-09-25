'''from django.db import models

class Userreg(models.Model):
    class Meta:
        db_table = "newuserref"
    uname = models.CharField(max_length=100)
    uemail = models.CharField(max_length=100)
    pwd = models.CharField(max_length=100)
    maritalstatus = models.CharField(max_length=100)
    gender = models.CharField(max_length=100) '''


from django.db import models

# Create your models here.


class t_user(models.Model):

    user_id = models.AutoField(primary_key = True)
    uname = models.CharField(max_length=200, unique=True)
    pwd = models.CharField(max_length=200)
    ufullname = models.CharField(max_length=200)
    uemail = models.EmailField(('email'), unique=True)
    unic = models.CharField(max_length=200)
    uaddress = models.CharField(max_length=200)
    utelephone = models.CharField(max_length=20)
    utype = models.CharField(max_length=20 )
    udob = models.DateField()
    verified = models.CharField(max_length=200 , default='yes')
    creation_date = models.DateField(auto_now_add=True)
    modification_date = models.DateField(auto_now=True)




class t_products(models.Model):
    product_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=200)

    description = models.CharField(max_length=400)
    enabled = models.CharField (max_length=200 , default='yes')
    creation_date = models.DateField(auto_now_add=True)
    modification_date = models.DateField(auto_now_add=True)

class t_product_provider(models.Model):
    t_product_provider_id = models.IntegerField(primary_key=True)
    enabled = models.CharField(max_length=10)
    rating = models.IntegerField(200)
    location = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    volunteer = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    long = models.IntegerField()
    width = models.IntegerField()
    creation_date = models.DateField()
    modification_date = models.DateField()

    user_id = models.ForeignKey(t_user,related_name='user', on_delete=models.PROTECT )
    product_id = models.ForeignKey(t_products,related_name='products', on_delete=models.CASCADE)

class t_announcements(models.Model):
    id =  models.IntegerField(primary_key=True)
    content = models.CharField(max_length=400)
    creation_date = models.DateField()
    modification_date = models.DateField()

    t_product_provider_id = models.ForeignKey(t_product_provider,related_name='productrovider2', on_delete=models.CASCADE)

class t_consumptions(models.Model):
    id = models.AutoField(primary_key = True)
    rating = models.IntegerField()
    status = models.CharField(max_length=20, default='Progress')
    enabled = models.CharField(max_length=10, default='yes')
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(auto_now_add=True)
    creation_date = models.DateField(auto_now_add=True)
    modification_date = models.DateField(auto_now_add=True)
    product_id = models.ForeignKey(t_products, related_name='product1',
                                              on_delete=models.CASCADE)
    user_id = models.ForeignKey(t_user, related_name='user1', on_delete=models.PROTECT)




class displaydata(models.Model):

    rating = models.CharField(max_length=100)
    location = models.CharField(max_length=100)





