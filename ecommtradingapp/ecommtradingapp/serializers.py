from rest_framework import serializers

from .models import t_user, t_products, t_product_provider, t_consumptions, t_announcements, displaydata


class T_userSerializer(serializers.ModelSerializer):
    class Meta:
        model = t_user
        fields = ('user_id','uname','pwd','uemail','ufullname','unic','uaddress','utelephone','utype','udob','verified','creation_date','modification_date')

class T_productSerializer(serializers.ModelSerializer):
    class Meta:
        model = t_products
        fields = ('product_id', 'name', 'description', 'enabled', 'creation_date', 'modification_date')

class T_product_providerSerializer(serializers.ModelSerializer):
    class Meta:
        model = t_product_provider
        fields = ('t_product_provider_id', 'enabled', 'rating', 'location', 'volunteer', 'description', 'long', 'width', 'creation_date', 'modification_date', 'product_id', 'user_id')

class T_consumptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = t_consumptions
        fields = ('id', 'rating', 'status', 'enabled', 'start_time', 'end_time', 'creation_date', 'modification_date', 'product_id', 'user_id')

class T_announcementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = t_announcements
        fields = ('id', 'content', 'creation_date', 'modification_date', 't_product_provider_id')

class T_consumptionproductProvider(serializers.ModelSerializer):
    class Meta:
        model = displaydata
        fields = ( 'rating','location')
