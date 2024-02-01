import mysql.connector
# from app import app, db

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password123",
    auth_plugin='mysql_native_password'
)

my_cursor = mydb.cursor()
# commented out to not accidently create another db
# my_cursor.execute("CREATE DATABASE wishlist")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)

# @app.cli.command()
# def initdb():
#     with app.app_context():
#         db.create_all()

# if __name__ == "__main__":
#     app.run()