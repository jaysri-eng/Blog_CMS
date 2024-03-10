from flask import Blueprint,request,jsonify,make_response
from flask_jwt_extended import jwt_required
from app import db
from blog.blog_model import Blog
from tag.tag_model import Tag

blogs= Blueprint('blogs',__name__)
@blogs.route('/add_post',methods=["POST"])
def create_blog():
    data = request.get_json()

    new_blog=Blog(title=data["title"],content=data["content"],image=data["image"])

    for tag in data["tags"]:
        current_tag=Tag.query.filter_by(name=tag).first()
        if(current_tag):
            current_tag.blogs_associated.append(new_blog)
        else:
            new_tag=Tag(name=tag)
            new_tag.blogs_associated.append(new_blog)
            db.session.add(new_tag)
            

    db.session.add(new_blog)
    db.session.commit()

    blog_id = getattr(new_blog, "id")
    return jsonify({"id": blog_id})

@blogs.route('/blogs',methods=["GET"])
def get_all_blogs():
    blogs= Blog.query.all()
    serialized_data = []
    for blog in blogs:
        serialized_data.append(blog.serialize)

    return jsonify({"all_blogs": serialized_data})

@blogs.route('/blog/<int:id>',methods=["GET"])
def get_single_blog(id):
    blog = Blog.query.filter_by(id=id).first()
    serialized_blog = blog.serialize
    serialized_blog["tags"] = []

    for tag in blog.tags:
        serialized_blog["tags"].append(tag.serialize)

    return jsonify({"single_blog": serialized_blog})

@blogs.route('/update_post/<int:id>', methods=["PUT"])
def update_post(id):
    data = request.get_json()
    blog=Blog.query.filter_by(id=id).first_or_404()

    blog.title = data["title"]
    blog.text=data["text"]
    blog.image=data["image"]

    updated_blog = blog.serialize

    db.session.commit()
    return jsonify({"blog_id": blog.id})

@blogs.route('/delete_post/<int:id>', methods=["DELETE"])
@jwt_required
def delete_post(id):
    blog = Blog.query.filter_by(id=id).first()
    db.session.delete(blog)
    db.session.commit()

    return jsonify("Blog was deleted"),200