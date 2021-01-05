from os import getenv
from flask import Flask, request, render_template, redirect, g 
from flask_login import login_required, current_user, login_user, logout_user
from .loginform import UserModel, db, login
from .forms import Mjrecomendationform

def create_app():
     # constructs core flask app, 
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLITE_DATABASE')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    from .loginform import db, login
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
            username = request.form['username']
            user = UserModel.query.filter_by(username = username).first()
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

    @app.route('/recomendations', methods=['GET', 'POST'])
    # def recomendations():
    #     return 'todo'
    def recomendations():
        search = Mjrecomendationform(request.form)
        if request.method == 'POST':
            return search_results(search)
        return render_template('recomendations.html', form=search)
    
    @app.route('/results')
    def search_results(search):
        results = []
        search_string = search.data['search']

        if search.data['search'] == '':
            qry = db_session.query(marijuana)
            results = qry.all()

        if not results:
            flash('no results found!')
            return redirect('/')
        else:
            return render_template('results.html', results=results)

        
    return app