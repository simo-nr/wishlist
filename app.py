from flask import Flask, render_template, url_for, request, redirect, session, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask import jsonify
from datetime import datetime
import uuid

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
    items = WishlistItem.query.filter_by(user=current_user).order_by(desc(WishlistItem.date_created)).all()
    return render_template('index.html', user=current_user.username, items=items)
    

@app.route('/view_user/<int:id>', methods=['POST', 'GET'])
@login_required
def view_user(id):
    viewing_user = load_user(id)
    if current_user == viewing_user:
        print("viewing user was equal")
        return redirect('/')
    items = WishlistItem.query.filter_by(user=viewing_user).order_by(desc(WishlistItem.date_created)).all()
    return render_template('view_user.html', items=items)


@app.route('/friends', methods=['POST', 'GET'])
@login_required
def friends():
    if request.method == 'POST':
        # TODO: change all of this, popup to add one friend

        # set everyone as friend for now
        all_users = User.query.all()
        for user in all_users:
            if user != current_user:
                current_user.friends.append(user)

    friend_users = current_user.friends
    return render_template('friends.html', friends=friend_users)


@app.route('/view_item/<int:id>', methods=['POST', 'GET'])
@login_required
def view_item(id):
    viewing_item = WishlistItem.query.get_or_404(id)
    return render_template('view_item.html', item=viewing_item, userId=current_user.id)


@app.route('/edit_item/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_item(id):
    edit_item = WishlistItem.query.get_or_404(id)
    owner_of_item = load_user(edit_item.user_id)

    if current_user != owner_of_item:
        print("user does not own item")
        return redirect('/')
    
    if request.method == 'POST':
        edit_item.name = request.form['name']
        edit_item.image_link = request.form['image_link']
        edit_item.url = request.form['url']
        edit_item.notes = request.form['notes']

        try:
            db.session.commit()
            print("item is changed")
            return render_template('view_item.html', item=edit_item)
        except:
            db.session.rollback()
            return "There was an error updating the item"
        
    return render_template('edit_item.html', item=edit_item)



@app.route('/new_url', methods=['POST', 'GET'])
@login_required
def new_url():
    if request.method == 'POST':
        item_url = request.form['url']
        
        # add web scraper here
        # to demonstrate webscraper, add notes
        notes = f'some things in the note to act like webscraper stuff {datetime.utcnow}'
        # for now just redirect to edit page with only the url in the item

        temp_new_item = WishlistItem(user_id=current_user.id, url=item_url, notes=notes)
        
        try:
            db.session.add(temp_new_item)
            db.session.commit()
            print("item added succesfully")
        except:
            db.session.rollback()
            print("item not added")
            return "there was a problem adding the item"

        return redirect(url_for('add_item', id=temp_new_item.id))
    
    return render_template('new_url.html')



@app.route('/add_item/<int:id>', methods=['POST', 'GET'])
@login_required
def add_item(id):
    new_item = WishlistItem.query.get(id)

    if new_item is None:
        print("item not found in the database")
        return "No item found in the database"

    if request.method == 'POST':
        new_item.name = request.form['name']
        new_item.image_link = request.form['image_link']
        new_item.url = request.form['url']
        new_item.notes = request.form['notes']

        try:
            db.session.add(new_item)
            db.session.commit()
            print("Item is added")
            return render_template('view_item.html', item=new_item)
        except:
            db.session.rollback()  # Rollback changes if an error occurs during commit
            return "There was an error updating the item"

    return render_template('add_item.html', item=new_item)




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