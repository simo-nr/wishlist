import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password123",
    database="wishlist",  # Specify the existing database name
    auth_plugin='mysql_native_password'
)

my_cursor = mydb.cursor()

# my_cursor.execute("SHOW DATABASES")
# for db in my_cursor:
#     print(db)

# Show all tables in the 'wishlist' database
my_cursor.execute("SHOW TABLES")
tables = my_cursor.fetchall()
for table in tables:
    print(table[0])

# Example: Add a new column 'new_column' to the 'WishlistItem' table
# my_cursor.execute("ALTER TABLE wishlist_item ADD COLUMN image_link VARCHAR(200)")
# my_cursor.execute("ALTER TABLE wishlist_item ADD COLUMN notes VARCHAR(400)")
my_cursor.execute("ALTER TABLE wishlist_item ADD COLUMN name VARCHAR(200)")
    
my_cursor.execute("ALTER TABLE user ADD COLUMN ")

mydb.commit()

# Verify the changes
my_cursor.execute("DESCRIBE wishlist_item")
for column in my_cursor:
    print(column)
