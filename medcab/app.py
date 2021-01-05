from os import getenv
from flask import Flask, request, render_template, redirect
from flask_login import login_required, current_user, login_user, logout_user
from .models import UserModel, db, login




def create_app():
     # constructs core flask app, with embedded dash app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLITE_DATABASE')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    from .models import db, login
    db.init_app(app)
    login.init_app(app)
    login.login_view = 'login' 
    

    @app.before_first_request
    def create_all():
        db.create_all()
       
    
    @app.route('/')
    @login_required
    def home():
        return render_template('home.html')

    @app.route('/login', methods = ['POST', 'GET'])
    def login():
        if current_user.is_authenticated:
            return redirect('/')
    
        if request.method == 'POST':
            email = request.form['email']
            user = UserModel.query.filter_by(email = email).first()
            if user is not None and user.check_password(request.form['password']):
                login_user(user)
                return redirect('/')
        return render_template('login.html')

    @app.route('/register', methods = ['POST', "GET"])
    def register():
        if current_user.is_authenticated:
            return redirect('/')
    
        if request.method == 'POST':
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
        
            if UserModel.query.filter_by(email = email).first():
                return('Email Already In Use')
        
            user = UserModel(email=email, username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect('/')
    
    @app.route('/recomendations')
    def recomendations():
        return f'"TODO FOR TOMORROW"'
    
    return app