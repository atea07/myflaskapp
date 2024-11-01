from app import app, db, bcrypt, login
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegisterForm, UpdateAccountForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
import os
from werkzeug.utils import secure_filename
from secrets import token_hex
from datetime import datetime, timezone

@login.user_loader
def load_user(id):
   return db.session.get(User, int(id))

@app.route('/')
def home():
    return render_template('home.html', title="Home")

@app.route('/list')
def index():
   users = User.query.all()
   return render_template('index.html', title="Users", users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
       return redirect(url_for('home'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
       user = User.query.filter_by(email = form.email.data).first()
       if user:
         #flash(f'User {user} is trying to login')
         if bcrypt.check_password_hash(user.password_hash, form.password.data):
           flash('Login succeeded')
           user.last_login = datetime.now(timezone.utc)
           db.session.commit()
           print(f'{user.last_login}')
           login_user(user)
           next_page = request.args.get('next')
           next_page = next_page if next_page else 'home'
           return redirect(str(next_page))   
       
       else:
          flash(f"User does not exist")
          return redirect(url_for('register')) 
    return render_template('login.html', form=form, title="Login")

@app.route('/logout')
def logout():
   flash('Logging out')
   logout_user()
   return redirect(url_for('index'))
   
@app.route('/register', methods=['GET', 'POST'])
def register():
   form = RegisterForm()
   if form.validate_on_submit():
      email = form.email.data
      user = User.query.filter_by(email=email).first()
      if user is not None:
         flash(f'{user} already exists. Please login.')
         return redirect(url_for('login'))
      password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      new_user = User(email=email, password_hash=password_hash)
      print(f'User {new_user} created.')
      db.session.add(new_user)
      db.session.commit()
      flash(f'User {new_user.email} is registered. Please login now')
      return redirect(url_for('login'))
   
   return render_template('register.html', form=form, title="Register", message="Register here")

   
@app.route('/user/<int:id>')
@login_required
def user(id:int):
   user = db.get_or_404(User,int(id))
   return render_template('user.html', user=user, title="User profile")

@app.route('/user/update', methods =['GET', 'POST'])
@login_required
def update_account():
   user = current_user
   form = UpdateAccountForm()
   if request.method == 'POST':
        pic_file = form.pic.data
        #print(dir(pic_file))
        flash(f"File uploaded")
        print(f"{pic_file.name}")
        _, file_ext = os.path.splitext(pic_file.name)
        new_picname = str(token_hex(8)) + file_ext
        flash(f'New filename {new_picname}')
        new_path = os.path.join(app.root_path, "static/images", new_picname)
        pic_file.save(new_path)
        user.pic_file =  os.path.join( "/static/images", new_picname)
        db.session.commit()
        return redirect(url_for('user', id=user.id))
   return render_template('account_update.html', form=form, title="Update account")
    
       
      
@app.errorhandler(404)
def user_error(e):
   return render_template('errors/404.html', title="404"), 404

@app.errorhandler(500)
def user_error(e):
   return render_template('errors/500.html', title="500"), 500