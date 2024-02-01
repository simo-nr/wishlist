
class Config:
    # local
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password123@localhost/wishlist'

    # live deployment on pythonanywhere
    # SQLALCHEMY_DATABASE_URI = 'mysql://Simon1122:password123password123@Simon1122.mysql.pythonanywhere-services.com/Simon1122$default'
    
    SECRET_KEY = 'hellothisisasecretkey' # TODO: set proper secret key

