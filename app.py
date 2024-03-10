from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from blog.blog_routes import blogs
import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from user.user_model import User

db = SQLAlchemy()


def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(blogs)
    app.config['JWT_SECRET_KEY']="walkers"
    jwt=JWTManager(app)
    CORS(app)
    db.init_app(app)
    @click.command(name='add_admin')   
    @with_appcontext
    def add_admin():
        admin=User(email="ADMIN EMAIL",password="YOUR PASSWORD STRING")
        admin.password = generate_password_hash(admin.password,'sha256',salt_length=12)
        db.session.add(admin)
        db.session.commit()

    app.cli.add_command(add_admin)
    
    return app

