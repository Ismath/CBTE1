import mysql.connector
import pandas as pd
my_conn = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database="cbte1_trading"
    )
t = 2
user = 'Colombo'
####### end of connection ####
my_data = pd.read_sql(" SELECT ecommtradingapp_t_products.name,ecommtradingapp_t_product_provider.location,count(*) from ecommtradingapp_t_consumptions inner join ecommtradingapp_t_product_provider on ecommtradingapp_t_consumptions.product_id_id = ecommtradingapp_t_product_provider.product_id_id inner join ecommtradingapp_t_products on ecommtradingapp_t_consumptions.product_id_id = ecommtradingapp_t_products.product_id where ecommtradingapp_t_consumptions.product_id_id = %s and ecommtradingapp_t_product_provider.location = %s and ecommtradingapp_t_consumptions.status ='Completed' group by ecommtradingapp_t_product_provider.location ",my_conn,params=(t,user))
my_data.to_excel('ds.xls')
print(my_data)