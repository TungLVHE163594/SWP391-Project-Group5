import random
import string

from models.user import Bookmark ,RoomRequest
from models.user import UserRole, User, HomeOwnerRequest, WebsiteFeedback
from models.model import db
from flask import Flask,redirect,url_for,json,render_template,request,session,flash
from flask_mail import Message
from controllers.mail_service import mail
from models.user import HomeOwnerRequest,User
from datetime import datetime
from models.post import  Post, PostImage
from models.report import ReportPost, ReportHome
from models.home import Home

def view_request_register():

    request_register = HomeOwnerRequest.query.all()
    return render_template("admin/view_request_register.html",request_register = request_register)

def allow_access():
    id = request.args.get("id")
    request_register = HomeOwnerRequest.query.filter_by(id = id).first()
    request_register.status = True
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
        return redirect( url_for('admin_router.reportedPosts') )
    return redirect( url_for('admin_router.reportedPosts') )

def accept_report():
    report_id = request.form.get("id")
    report = ReportPost.query.filter_by(id = report_id).first()
    if report:
        db.session.delete(report)
        db.session.commit()
        
    postID = report.post_id
    post_img = PostImage.query.filter_by(post_id = postID).first()
    if post_img:
        # for img in post_img:
            db.session.delete(post_img)
            db.session.commit()
            
    post = Post.query.filter_by(id = postID).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        return redirect( url_for('admin_router.reportedPosts') )
    return redirect( url_for('admin_router.reportedPosts') )

def view_feedback():
    feedback_list = WebsiteFeedback.query.all()
    for feedback in feedback_list:
        feedback.username = User.query.filter_by(id = feedback.user_id).first().username
    return render_template("admin/view_feedback.html",feedback_list = feedback_list)

def reported_Homes():
    page = request.args.get('page', 1, type=int)
    number = ReportHome.query.count()
    homes = ReportHome.query.order_by(ReportHome.timestamp.desc()).paginate(page=page, per_page=5)
    return render_template('admin/reported_home.html', homes=homes, counter=number)

def delete_home_report():
    report_id = request.form.get("id")
    report = ReportHome.query.filter_by(id = report_id).first()
    if report:
        db.session.delete(report)
        db.session.commit()
        return redirect( url_for('admin_router.reportedHomes') )
    return redirect( url_for('admin_router.reportedHomes') )

    