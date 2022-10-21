import random
import string
from models.user import Bookmark ,RoomRequest
from models.user import UserRole, User, HomeOwnerRequest
from models.model import db
from flask import Flask,redirect,url_for,json,render_template,request,session,flash
from flask_mail import Message
from controllers.mail_service import mail
from models.user import HomeOwnerRequest,User
from datetime import datetime
from models.post import  Post
from models.report import ReportPost
from models.post import PostImage

def view_request_register():

    request_register = HomeOwnerRequest.query.all()
    return render_template("admin/view_request_register.html",request_register = request_register)

def refuse_access():
    id = request.args.get("id")
    home_owner_request = HomeOwnerRequest.query.filter_by(id = id).first()
    
    user = User.query.filter_by(id = home_owner_request.user_id).first()

    
    db.session.delete(home_owner_request)
    db.session.commit()
    
    return redirect(url_for("admin_router.view_request_register"))

def reported_Posts():
    page = request.args.get('page', 1, type=int)
    number = ReportPost.query.count()
    reported_posts = ReportPost.query.order_by(ReportPost.timestamp.desc()).paginate(page=page, per_page=5)
    return render_template('post/reported_post.html', posts=reported_posts, counter=number)

def delete_report():
    report_id = request.form.get("id")
    report = ReportPost.query.filter_by(id = report_id).first()
    if report:
        db.session.delete(report)
        db.session.commit()
        return redirect( url_for('post_router.reportedPosts') )
    return redirect( url_for('post_router.reportedPosts') )

def accept_report():
    report_id = request.form.get("id")
    report = ReportPost.query.filter_by(id = report_id).first()
    if report:
        db.session.delete(report)
        db.session.commit()
        
    postID = report.post_id
    post_img = PostImage.query.filter_by(post_id = postID).first()
    if post_img:
        for img in post_img:
            db.session.delete(img)
            db.session.commit()
            
    post = Post.query.filter_by(id = postID).first()
    if report:
        db.session.delete(post)
        db.session.commit()
        return redirect( url_for('post_router.reportedPosts') )
    return redirect( url_for('post_router.reportedPosts') )