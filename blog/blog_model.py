from app import db
from datetime import datetime
from blog_tags.blog_tag_table import tag_blog

tags=db.relationship('Tag',secondary=tag_blog,backref=db.backref('blogs_associated',lazy="dynamic"))

class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    text=db.Column(db.Text,nullable=False)
    image= db.Column(db.String,nullable=False)
    date_of_publish = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'image': self.image,
            'date_of_publish': self.date_of_publish,
        }