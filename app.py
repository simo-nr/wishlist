from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask import jsonify
from flask_wtf.csrf import CSRFProtect, CSRFError
from datetime import datetime

from config import Config
from models import db, User, WishlistItem


app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object(Config)

db.init_app(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        print(f"user after login in {user}")
        print(f"password {password}")
        if user and bcrypt.check_password_hash(user.password, password):
            print("inside if, user was not null and password was verified")
            login_user(user)
            return redirect(url_for('index'))
        else:
            print("password not verified or user was null")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username is already taken. Choose a different one."
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        print(f"hashed password: {hashed_password}")

        new_user = User(username=username, password=hashed_password)
        print(f"new user: {new_user}")
        try:
            db.session.add(new_user)
            db.session.commit()
            # login_user(new_user)  # Log in the new user automatically after registration
            # return redirect(url_for('index'))
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error registering user: {e}")
            return "There was an error during registration."

    return render_template('register.html')
    

@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        item_url = request.form['url']
        new_item = WishlistItem(url=item_url, user=current_user)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding the item"
    else:
        # items = WishlistItem.query.order_by(WishlistItem.date_created).all()
        items = WishlistItem.query.filter_by(user=current_user).order_by(WishlistItem.date_created).all()
        return render_template('index.html', items = items)
    

@app.route('/view/<int:id>', methods=['POST', 'GET'])
@login_required
def view(id):
    viewing_user = load_user(id)
    if current_user == viewing_user:
        print("viewing user was equal")
        return redirect('/')
    items = WishlistItem.query.filter_by(user=viewing_user).order_by(WishlistItem.date_created).all()
    return render_template('view.html', items = items)


@app.route('/checkoff/<int:item_id>', methods=['POST'])
@login_required
def check_off_item(item_id):
    try:
        item = WishlistItem.query.get_or_404(item_id)
        item.checked_off = True
        db.session.commit()
        return jsonify({'message': 'Item checked off successfully'})
    except CSRFError as e:
        return jsonify({'error': 'CSRF token validation failed'}), 400  # Return a 400 Bad Request status for CSRF errors



# Function to create the app context
def create_app():
    return app
# Command to create the database tables
@app.cli.command("initdb")
def initdb_command():
    with app.app_context():
        db.create_all()
    print("Initialized the database.")

if __name__ == "__main__":
    app.run(debug=True)