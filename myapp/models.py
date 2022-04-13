from myapp import app,db
from datetime import datetime
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user, roles_accepted
from flask_admin import Admin, BaseView, expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import event
from slugify import slugify

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    slug = db.Column(db.String(180), nullable=False)
    body = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150), nullable=False, default='no-image.jpg')
    category=db.Column(db.String(200),nullable=False)
    comments = db.Column(db.Integer,default=0)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    author = db.relationship('User', backref=db.backref(
        'posts', lazy=True, passive_deletes=True))
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r' % self.title
    @staticmethod
    def generat_slug(target,value,oldvalue,initiator):
        if value and (not target.slug or value !=oldvalue):
            target.slug=slugify(value)
db.event.listen(Post.title,'set',Post.generat_slug,retval=False)



class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=False, nullable=False)
    email = db.Column(db.String(200), unique=False, nullable=False)
    message = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    post = db.relationship('Post', backref=db.backref('posts',lazy=True, passive_deletes=True))
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(120), unique=True)
    email = db.Column(db.String(255))
    subject=db.Column(db.Text, nullable=False)
    message= db.Column(db.Text, nullable=False)
    user_message=db.relationship('User', backref=db.backref('contact_message',lazy=True, passive_deletes=True))
    user_id_contact=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class UserView(ModelView):
    pass

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

class RoleView(ModelView):
    pass
class PostView(ModelView):
    pass
class CommentView(ModelView):
    pass
class ContactView(ModelView):
    pass
