import pandas as pd
import mysql.connector
import os
import seaborn as sns
import matplotlib.pyplot as plt

# List of CSV files and their corresponding table names
# csv_files = [
#     ('customers.csv', 'customers'),
#     ('orders.csv', 'orders'),
#     ('sellers.csv', 'sellers'),
#     ('products.csv', 'products'),
#     ('geolocation.csv', 'geolocation'),
#     ('payments.csv', 'payments'),
#     ('order_items.csv', 'order_items')
# ]
#
# # Connect to the MySQL database
# conn = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='Sumit_123',
#     database='ecommerce'
# )
# cursor = conn.cursor()
#
# # Folder containing the CSV files
# folder_path = 'C:/Users/Sumit Sinha/Desktop/DataAnalysisProject_OrderSeller/DataSets'
#
#
# def get_sql_type(dtype):
#     if pd.api.types.is_integer_dtype(dtype):
#         return 'INT'
#     elif pd.api.types.is_float_dtype(dtype):
#         return 'FLOAT'
#     elif pd.api.types.is_bool_dtype(dtype):
#         return 'BOOLEAN'
#     elif pd.api.types.is_datetime64_any_dtype(dtype):
#         return 'DATETIME'
#     else:
#         return 'TEXT'
#
#
# for csv_file, table_name in csv_files:
#     file_path = os.path.join(folder_path, csv_file)
#
#     # Read the CSV file into a pandas DataFrame
#     df = pd.read_csv(file_path)
#
#     # Replace NaN with None to handle SQL NULL
#     df = df.where(pd.notnull(df), None)
#
#     # Debugging: Check for NaN values
#     print(f"Processing {csv_file}")
#     print(f"NaN values before replacement:\n{df.isnull().sum()}\n")
#
#     # Clean column names
#     df.columns = [col.replace(' ', '_').replace('-', '_').replace('.', '_') for col in df.columns]
#
#     # Generate the CREATE TABLE statement with appropriate data types
#     columns = ', '.join([f'`{col}` {get_sql_type(df[col].dtype)}' for col in df.columns])
#     create_table_query = f'CREATE TABLE IF NOT EXISTS `{table_name}` ({columns})'
#     cursor.execute(create_table_query)
#
#     # Insert DataFrame data into the MySQL table
#     for _, row in df.iterrows():
#         # Convert row to tuple and handle NaN/None explicitly
#         values = tuple(None if pd.isna(x) else x for x in row)
#         sql = f"INSERT INTO `{table_name}` ({', '.join(['`' + col + '`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(row))})"
#         cursor.execute(sql, values)
#
#     # Commit the transaction for the current CSV file
#     conn.commit()
#
# # Close the connection
# conn.close()

db=mysql.connector.connect(host="localhost", username="root", password="Sumit_123", database="ecommerce")
cur = db.cursor()
print("\nEnd-to-End SQL-Python Data Analytics Project.")
print("---------------------------------------------")
print("\n")

# 1. List all unique cities where customers are located.
query = """ select distinct customer_city from customers """
cur.execute(query)
data=cur.fetchall()
df=pd.DataFrame(data)
print("All cities where customers are located.")
print(df.head())

# 2. Count the number of orders placed in 2017.
query = """ select count(order_purchase_timestamp) from orders where year(order_purchase_timestamp) = 2017 """
cur.execute(query)
data = cur.fetchall()
print("\ntotal orders placed in 2017 are", data[0][0])

# 3. Find the total sales per category.
query = """ select products.product_category, sum(payments.payment_value) 
from products join order_items on products.product_id=order_items.product_id join payments on 
payments.order_id=order_items.order_id group by products.product_category """
cur.execute(query)
data = cur.fetchall()
print(pd.DataFrame(data))

# 4. Calculate the percentage of orders that were paid in installments.
query = """ select (sum(payment_installments>=1)/count(*))*100 from payments; """
cur.execute(query)
data = cur.fetchall()
print(pd.DataFrame(data))

# 5. Count the number of customers from each state.
query = """ select count(customer_id), customer_state from customers group by customer_state; """
cur.execute(query)
data = cur.fetchall()
print(pd.DataFrame(data))

# 6. Calculate the number of orders per month in 2018.
query = """select monthname(order_purchase_timestamp), count(monthname(order_purchase_timestamp))  
from orders where year(order_purchase_timestamp)=2018 group by monthname(order_purchase_timestamp);"""
cur.execute(query)
data = cur.fetchall()
print(pd.DataFrame(data))

#7. Find the average number of products per order, grouped by customer city.
query=""" with count_per_order as 
(select orders.order_id, orders.customer_id, count(order_items.order_id) as oc
from orders join order_items on orders.order_id = order_items.order_id
group by orders.order_id, orders.customer_id)
select customers.customer_city, round(avg(count_per_order.oc),2) average_orders
from customers join count_per_order on customers.customer_id = count_per_order.customer_id
group by customers.customer_city order by average_orders desc """
cur.execute(query)
data = cur.fetchall()
print(pd.DataFrame(data))

#8. Calculate the percentage of total revenue contributed by each product category.
query="""select(products.product_category), sum(payments.payment_value)/(select sum(payment_value) from payments)*100
from products join order_items on products.product_id=order_items.product_id join payments 
on payments.order_id = order_items.order_id group by products.product_category"""
cur.execute(query)
data = cur.fetchall()
print(pd.DataFrame(data))

#9. Identify the correlation between product price and the number of times a product has been purchased.
query = """ select products.product_category, count(order_items.product_id), avg(order_items.price)
from products join order_items on products.product_id = order_items.product_id group by products.product_category """
cur.execute(query)
data = cur.fetchall()
print(pd.DataFrame(data))

#10. Calculate the total revenue generated by each seller, and rank them by revenue.
query = """select *, dense_rank() over(order by revenue desc) as rn from (select order_items.seller_id, sum(payments.payment_value)
revenue from order_items join payments on order_items.order_id = payments.order_id group by order_items.seller_id) as a"""
cur.execute(query)
data = cur.fetchall()
print(pd.DataFrame(data))

#11. Calculate the moving average of order values for each customer over their order history.
query = """select customer_id, order_purchase_timestamp, payment,
avg(payment) over(partition by customer_id order by order_purchase_timestamp rows between 2 preceding and current row) as mov_avg
from (select orders.customer_id, orders.order_purchase_timestamp, payments.payment_value as payment
from payments join orders on payments.order_id = orders.order_id) as a"""
cur.execute(query)
data = cur.fetchall()
print(pd.DataFrame(data))

#12. Calculate the cumulative sales per month for each year.
query = """ select years, months , payment, sum(payment) over(order by years, months) cumulative_sales from 
(select year(orders.order_purchase_timestamp) as years, month(orders.order_purchase_timestamp) as months,
round(sum(payments.payment_value),2) as payment from orders join payments
on orders.order_id = payments.order_id group by years, months order by years, months) as a """
cur.execute(query)
data = cur.fetchall()
print(pd.DataFrame(data))

print("\n")
print("--------------------------------------------------------------")
print("Completion of an SQL-Python end-to-end Data Analysis Project.")