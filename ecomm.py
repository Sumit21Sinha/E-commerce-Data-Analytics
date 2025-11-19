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

# 1. List all unique cities where customers are located.
query = """ select distinct customer_city from customers """
cur.execute(query)
data=cur.fetchall()
df=pd.DataFrame(data)
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
query = """  """
cur.execute(query)
data = cur.fetchall()
print(pd.DataFrame(data))