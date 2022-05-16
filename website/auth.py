from email.policy import strict
from unittest import result
from flask import Flask, jsonify
from flask import Blueprint,render_template, request,flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import requests
from .models import *
from .models import db
from requests import  get
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
ma = Marshmallow(app)
db.init_app(app)

app.config['SECRET_KEY'] = "groupe5"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:groupe5@localhost/template1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 
auth = Blueprint('auth', __name__)

class geoSchema(Schema):
      lat = fields.String()
      lng = fields.String()

class addressSchema(Schema):
      street = fields.String()
      suite = fields.String()
      city = fields.String()
      zipcode = fields.String()
      geo = fields.Nested(geoSchema)


class companySchema(Schema):
      name_company = fields.String()
      catchPhrase =  fields.String()
      bs = fields.String()

class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    username = fields.String()
    email = fields.String()
    phone = fields.String()
    website = fields.String()
    address = fields.Nested(addressSchema)
    company = fields.Nested(companySchema)
   


   



class postsSchema(ma.Schema):
       class Meta:
              fields = ("id","title","body","userId")
postSchema = postsSchema(many = True)
class albumsSchema(ma.Schema):
       class Meta:
              fields = ("id","title","userId")
albumSchema = albumsSchema(many = True)
class commentsSchema(ma.Schema):
       class Meta:
              fields = ("id","name","email","body","postId")
commentSchema = commentsSchema(many = True)
class todosSchema(ma.Schema):
       class Meta:
              fields = ("id","title","completed","userId")
todoSchema = todosSchema(many = True)
class photosSchema(ma.Schema):
       class Meta:
              fields = ("id","title","url","thumbnailUrl","albumId")
photoSchema = photosSchema(many = True)

@auth.route("/comments", methods = ["GET"])
def comments():
      comments = Comments.query.all()
      result = commentSchema.dump(comments)
      return jsonify(result)


@auth.route("/users", methods = ["GET"])
def users():
      users = Users.query.all()
      result = UserSchema.dumps(users)
      return jsonify(result)


@auth.route("/todos", methods = ["GET"])
def todos():
      todos = Todos.query.all()
      result = todoSchema.dump(todos)
      return jsonify(result)


@auth.route("/photos", methods = ["GET"])
def photos():
      photos = Photos.query.all()
      result = photoSchema.dump(photos)
      return jsonify(result)


@auth.route("/posts", methods = ["GET"])
def posts():
      posts = Posts.query.all()
      result = postSchema.dump(posts)
      return jsonify(result)


@auth.route("/albums", methods = ["GET"])
def albums():
      albums = Albums.query.all()
      result = albumSchema.dump(albums)
      return jsonify(result)


       

@auth.route("/", methods = ["GET","POST"])
def home():
  load_data("users")
  load_data("albums")
  load_data("posts")
  load_data("comments")
  load_data("photos")
  load_data("todos")

  return render_template("home.html")




































































def searchapi(end):
    url = get('https://jsonplaceholder.typicode.com/'+end)
    return url.json()


def load_data(type):
    if type == 'users':
         
      users_from_apis= searchapi('users')

      for data in users_from_apis:
            perso = Users(id = data.get("id"),
               name = data.get("name"), 
                              username = data.get("username"), email = data.get("email"), 
                              phone = data.get("phone"),
                              website = data.get("website"), street = data["address"]["street"],
                              suite = data["address"]["suite"], 
                              city = data["address"]["city"],zipcode = data["address"]["zipcode"],
                              lng = data["address"]["geo"]["lat"], lat = data["address"]["geo"]["lat"],
                              name_company = data["company"]["name"], catchPrase = data["company"]["catchPhrase"],
                              bs = data["company"]["bs"])
            
            db.session.add(perso)
      db.session.commit()
            
    elif  type == 'posts':
        
        posts_from_apis= searchapi('posts') 

        for post in posts_from_apis:
            posts = Posts(
                id = post.get('id'),
                title = post.get('title'), 
                body = post.get('body'), 
                userId = post.get("userId")
            )

            db.session.add(posts)
        db.session.commit()
           
    elif type == "comments":
           
            comments_from_apis=searchapi('comments')

            for comment in comments_from_apis:
              
                comments = Comments(
                    id = comment.get("id"),
                    name = comment.get('name'), 
                    body= comment.get('body'),
                    email = comment.get('email'),
                    postId =comment.get("postId")
                )
         
            
                db.session.add(comments)
            db.session.commit()
      
       
    
    elif type == 'todos':
        todos = searchapi('todos')
        for todo in todos:
            todos = Todos(
            id = todo.get("id"),
            userId = todo.get("userId"),
            title =todo.get("title"),
            completed = todo.get("completed"))
            
       
            db.session.add(todos)
        db.session.commit()
            
    elif type == 'albums':
        albums_from_apis =searchapi('albums') 

        for album in albums_from_apis:
            albums = Albums(
                id = album.get('id'),
                title = album.get('title'),
                userId = album.get('userId')
               )
            
            db.session.add(albums)
        db.session.commit()
       
    elif type == 'photos':
            photos_from_apis= searchapi('photos')
            for photo in photos_from_apis:
                photos= Photos(
                    id = photo.get("id"),
                    albumId = photo.get("albumId"), 
                    title = photo.get("title"),
                    url = photo.get("url"),
                    thumbnailUrl = photo.get("thumbnailUrl"))
              
                db.session.add(photos)
            db.session.commit()
      
       
  
