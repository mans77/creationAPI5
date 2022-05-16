from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = "groupe5"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:groupe5@localhost/template1'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    


    from .auth import auth

    app.register_blueprint(auth, url_prefix  ="/")
    
    
    return app 

        
        

    