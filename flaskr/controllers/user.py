import random
import string
from models.user import Bookmark ,RoomRequest
from models.user import UserRole, User, HomeOwnerRequest
from models.model import db
from flask import Flask,redirect,url_for,json,render_template,request,session,flash
from flask_mail import Message
from controllers.mail_service import mail
from models.post import Post
from datetime import datetime


def home():
    if "username" in session:
        user = session['username']
        return render_template("home.html", username = user, isLogin = True)
    else:
        return render_template("home.html", stringName = "you are not login", isLogin = False)

def login():
    user_name = request.form["user"]
    pass_word = request.form["pass"]
    query = User.query.filter(User.username == user_name , User.password == pass_word).first()
    if query:
        session['username'] = query.username
        session['id'] = query.id
        session['role'] = query.role
        session['banned'] = query.banned
        session['email'] = query.email
        return redirect(url_for("user_router.home"))
    flash("Your account doesn't exist","info")
    return render_template("login.html")


def logout():
    session.clear()
    return redirect(url_for('user_router.home'))

def forgot_password(email):
    # kiem tra email
    user = db.session.execute(db.select(User).where(User.email == email)).first()
    if user != None:
        # gen new password
        new_password = gen_new_password()
        # update password
        user[0].password = new_password
        # luu password moi vao database
        db.session.commit()
        #send email
        msg = Message('Your new password is: ' + new_password, sender = 'sweethomehola@outlook.com', recipients = [email])
        mail.send(msg)

        #thong bao toi front end
        flash("New password has been sent to your email.","info")
        return render_template("login.html")
    else:
        flash("Wrong email!","info")
        return render_template("forgot_password.html")

def check_exist_user(username, email):
    user = db.session.execute(db.select(User).where(User.username == username)).first()
    if user:
        return True
    user = db.session.execute(db.select(User).where(User.email == email)).first()
    if user:
        return True
    return False

def register(username, password, email):
    # kiem tra du lieu
    if not check_exist_user(username, email):
    # add vao database
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        session['id'] = user.id
        session['role'] = user.role
        session['banned'] = user.banned
        session['email'] = user.email
        return redirect(url_for('user_router.home'))
    else:
        flash("duplicate email or username", "info")
        return render_template("register.html")

def register_seller(username, email):
    # kiem tra du lieu
    if not check_exist_user(username, email):
        password = gen_new_password()
        # add vao database
        user = User(username=username, password=password, email=email, role=UserRole.SELLER, banned=True)
        db.session.add(user)
        user = User.query.filter(User.username == username).first()

        user_request = HomeOwnerRequest(user_id=user.id, home_id = 1)
        db.session.add(user_request)
        db.session.commit()
        
        flash("Your request has been sent to admin. Please wait for approval, we will send password in your email.","info")
        return render_template("register_seller.html")
    else:
        flash("duplicate email or username", "info")
        return render_template("register_seller.html")

def gen_new_password():
    password = ''
    for i in range(8):
        password += random.choice(string.ascii_letters + string.digits + string.punctuation)
    return password

def profile():
    user = User.query.filter(User.id == session['id']).first()
    username = user.username
    email = user.email
    return render_template("userProfile.html",username=username,email=email)

def edit_profile():
    user = User.query.filter(User.id == session['id']).first()
    checkUsername = User.query.filter(User.username == request.form["username"]).first()
    if checkUsername:
        flash("Username already exists!","info")
        return render_template("editProfile.html",username=user.username,email=user.email)
    checkEmail = User.query.filter(User.email == request.form["email"]).first()
    if checkEmail:
        flash("Email already exists!","info")
        return render_template("editProfile.html",username=user.username,email=user.email)
    user.username = request.form["username"] if request.form["username"] != "" else user.username
    session['username'] = user.username
    user.email = request.form["email"] if request.form["email"] != "" else user.email
    db.session.commit()
    # return render_template("userProfile.html",username=user.username,email=user.email)
    return redirect(url_for('user_router.profile'))

def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author_id=user.id)\
        .order_by(Post.timestamp.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

def bookmark(userid):
    bookmarks = Bookmark.query.filter(User.id == userid).all()
    # missing liked posts
    if bookmarks:
        return render_template("bookmark.html",bookmarks=bookmarks)
    flash("You don't have any bookmark yet!","info")
    return render_template("bookmark.html")

def add_room_request():
    name = request.form['name']
    phone = request.form['phone']
    timeVisit = request.form['timeVisit']
    user_id = session["id"]
    timestamp = datetime.now()
    content = "Name: " + name + " Phone: " + phone + " Time visit: " + timeVisit
    room_reqest = RoomRequest(user_id = user_id, content = content, timestamp = timestamp)
    db.session.add(room_reqest)
    db.session.commit()
    return render_template("roomRequest.html", done = True, name = name, phone = phone, timeVisit = timeVisit)