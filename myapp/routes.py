import os
import secrets
from flask import Flask,render_template,request,url_for,redirect,current_app,flash
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user, roles_accepted
from myapp import app,db
from myapp.models import User,Post,Role,Comments,Contact
from datetime import datetime


def create_user():
    user=User.query.filter(User.email == 'fawiw56253@rvemold.com').first()
    user.roles.append(Role(name='admin'))
    db.session.add(user)
    db.session.commit()

def save_images(photo):
    hash_photo=secrets.token_urlsafe(10)
    _,file_extention=os.path.splitext(photo.filename)
    photo_name=hash_photo+file_extention
    file_path=os.path.join(current_app.root_path,'static/image',photo_name)
    photo.save(file_path)
    return photo_name

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_pub.desc()).paginate(page=page, per_page=6)
    return render_template('index.html',posts=posts)


@app.route('/addpost',methods=['GET','POST'])
def addpost():
    if request.method=="POST":
        title=request.form['title']
        photo=save_images(request.files.get('photo'))
        body=request.form['body']
        catagory=request.form['catagory']
        post=Post(title=title,image=photo, body=body,author=current_user,category=catagory)
        db.session.add(post)
        db.session.commit()
        flash("New post has been created","success")
        return redirect(url_for("index"))
    return render_template('addnewpost.html')

@app.route('/post/<int:post_id>/<string:slug>',methods=['GET','POST'])
def post(post_id,slug):
    post=Post.query.get_or_404(post_id)
    comments=Comments.query.filter_by(post_id=post.id).all()
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        message=request.form['message']
        comment=Comments(username=username,email=email,message=message,post_id=post.id)
        db.session.add(comment)
        post.comments+=1
        flash('Your comment has been posted!','success')
        db.session.commit()
        return redirect(request.url)
    random_posts=Post.query.order_by(db.func.random()).limit(18).all()

    return render_template('postdetails.html',post=post,comments=comments,random_posts=random_posts)

@app.route('/contact',methods=['POST','GET'])
@login_required
def contact():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        message=request.form['message']
        contact=Contact(username=username,email=email,message=message,user_id_contact=current_user.id)
        db.session.add(contact)
        flash("We have recieved your message.We will reply you quickly.","success")
        db.session.commit()
        return redirect(request.url)
    return render_template('contact.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/arduino')
def arduino():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="arduino").order_by(Post.date_pub.desc()).paginate(page=page, per_page=6)
    return render_template('arduino.html',posts=posts)

@app.route('/robotics')
def robotics():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="robotics").order_by(Post.date_pub.desc()).paginate(page=page, per_page=6)
    return render_template('robotics.html',posts=posts)

@app.route('/iot')
def iot():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="iot").order_by(Post.date_pub.desc()).paginate(page=page, per_page=6)
    return render_template('iot.html',posts=posts)

@app.route('/biomedical')
def biomedical():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="bio").order_by(Post.date_pub.desc()).paginate(page=page, per_page=6)
    return render_template('biomedical.html',posts=posts)
@app.route('/rfid')
def rfid():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="rfid").order_by(Post.date_pub.desc()).paginate(page=page, per_page=6)
    return render_template('rfid.html',posts=posts)

@app.route('/electrical')
def electrical():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="electrical").order_by(Post.date_pub.desc()).paginate(page=page, per_page=6)
    return render_template('electrical.html',posts=posts)


@app.route('/updatepost/<id>',methods=['POST','GET'])
def updatepost(id):
    post=Post.query.get_or_404(id)
    if request.method=="POST":
        if request.files.get('photo'):
            try:
                os.unlink(os.path.join(current_app.root_path,'static/image/'+post.image))
                post.image=save_images(request.files.get('photo'))
            except:
                post.image=save_images(request.files.get('photo'))
        post.title=request.form['title']
        post.body=request.form['body']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editpost.html',post=post)

@app.route('/delete/<id>',methods=['POST','GET'])
@login_required
def delete(id):
    post=Post.query.get_or_404(id)
    try:
        os.unlink(os.path.join(current_app.root_path,'static/image/'+post.image))
        db.session.delete(post)
        
    except:
        db.session.delete(post)
        
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=="POST":
        word = request.form["tag"]
        result = "%{}%".format(word)
        posts = Post.query.filter(Post.title.like(result)).all()
    
    
    return render_template('search.html',posts=posts)

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def error_500(error):

    return render_template('errors/500.html'), 500
