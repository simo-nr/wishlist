from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask import jsonify
from datetime import datetime

from config import Config
from models import db, User, WishlistItem


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


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
    items = WishlistItem.query.filter_by(user=current_user).order_by(WishlistItem.date_created).all()
    return render_template('index.html', user=current_user.username, items=items)
    

@app.route('/view_user/<int:id>', methods=['POST', 'GET'])
@login_required
def view_user(id):
    viewing_user = load_user(id)
    if current_user == viewing_user:
        print("viewing user was equal")
        return redirect('/')
    items = WishlistItem.query.filter_by(user=viewing_user).order_by(WishlistItem.date_created).all()
    return render_template('view_user.html', items=items)

@app.route('/view_item/<int:id>', methods=['POST', 'GET'])
@login_required
def view_item(id):
    viewing_item = WishlistItem.query.get_or_404(id)
    return render_template('view_item.html', item=viewing_item)

@app.route('/edit_item/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_item(id):
    edit_item = WishlistItem.query.get_or_404(id)
    owner_of_item = load_user(edit_item.user_id)
    if current_user != owner_of_item:
        print("user does not own item")
        return redirect('/')
    return render_template('edit_item.html', item=edit_item)

@app.route('/new', methods=['POST', 'GET'])
@login_required
def new():
    if request.method == 'POST':
        item_url = request.form['url']
        new_item = WishlistItem(url=item_url, user=current_user)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding the item"
    return render_template('new.html')


@app.route('/checkoff/<int:item_id>', methods=['POST'])
@login_required
def check_off_item(item_id):
    item = WishlistItem.query.get_or_404(item_id)
    item.checked_off = True
    db.session.commit()
    return jsonify({'message': 'Item checked off successfully'})


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