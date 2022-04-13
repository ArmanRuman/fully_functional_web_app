import os
import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user, roles_accepted
from flask_mail import Mail
from flask_share import Share
from flask_admin import Admin, BaseView, expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fbejkwfbuewfbweipbgweibgiwjebfweupfbgpuebeb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/myprojectguide'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
share = Share(app)
from myapp.models import User,Role,Post,Comments,Contact,MyAdminIndexView,UserView
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'mysalt'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = True
app.config['SECURITY_EMAIL_SUBJECT_REGISTER']='Welcome you from projectguidebd.com!'
app.config['SECURITY_POST_LOGOUT_VIEW']='login'
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_POST_REGISTER_VIEW']='login'
app.config['SECURITY_EMAIL_SENDER'] = 'projectguide00@gmail.com'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'projectguide00@gmail.com'
app.config['MAIL_PASSWORD'] = 'projectguide00@@'
app.config['MAIL_USE_TLS'] = False 
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER']=('Arman','projectguide00@gmail.com')
mail = Mail(app)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
admin = Admin(app,name='projectguide.com', template_mode='bootstrap3',index_view=MyAdminIndexView())
admin.add_view(UserView(User, db.session))
admin.add_view(UserView(Role, db.session))
admin.add_view(UserView(Post, db.session))
admin.add_view(UserView(Comments, db.session))
admin.add_view(UserView(Contact, db.session))

from myapp import routes