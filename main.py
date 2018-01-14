from flask import Flask, request, redirect, render_template, session,flash
import cgi
from flask_sqlalchemy import SQLAlchemy
from validateCode import * # this file contians all the verification codes
from datetime import datetime



app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:beHappy@localhost:8889/Blogz'
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)
app.secret_key = "XzP&31d2arfs&9!4"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),unique=True) #unique
    hashPassword = db.Column(db.String(120))
    saltPassword = db.Column(db.String(5))
    email = db.Column(db.String(120))

    record = db.Column(db.String(40))
    blogs = db.relationship('Blog', backref='owner') # links class Blog to class User  

    def __init__(self, username,hashPassword, saltPassword, email = None):
        self.username = username
        self.hashPassword = hashPassword
        self.saltPassword = saltPassword
        self.email = email
        self.record = datetime.now().strftime("%m - %d- %Y %H:%M:%S")



class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True) #unique
    body = db.Column(db.String(1000))
    record = db.Column(db.String(40))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) # links class Blog to class User 

    def __init__(self, title, body, owner):
        self.title = title
        self.body =body
        self.record = datetime.now().strftime("%m - %d- %Y %H:%M:%S")
        self.owner = owner





@app.route("/signUp")
def signUpPage():
    return render_template("signUp.html")


@app.route("/validate_signUP", methods = ["POST"])
def validateSignUp():
    userName = request.form["username"]
    passWord = request.form["password"]
    passWord2 = request.form["password2"]
    email = request.form["email"]
    if verifyUserName(userName) and verifyPassword(passWord,passWord2) and verifyEmail(email):
        duplicate= ""
        if not User.query.filter_by(username = userName).first():
            hashedPassword, salt = hashPassword(passWord)
            new_user = User( userName, hashedPassword, salt)
            db.session.add(new_user)
            db.session.commit()
            session["user"] = userName
            return redirect ("/welcome")
        else:
            duplicate = "User Name not avaliable. Please Choose a different User Name"
     
    error1 = ""
    error2 = ""
    error3 = ""
    if not verifyUserName(userName):
        error1 = "invalid username"
    if not verifyPassword(passWord, passWord2):
        error2 = "invalid password"
    if not verifyEmail(email):
        error3 = "invalid email address"    

    return render_template("signUp.html", duplicate_error = duplicate, password_error = error2, name_error = error1, email_error = error3)


#welcome message after login
@app.route("/welcome")
def welcomeMsg():
    return "Welcome, congrats you signed up"




@app.before_request
def require_login():
    allowed_routes = ["loginPage","signUpPage","validateLogin","validateSignUp"]
    if request.endpoint not in allowed_routes and "user" not in session:
        return redirect("/")

# shows the login page as the default page before login
@app.route("/")
def loginPage():
    return render_template("login.html")


# validates login
@app.route("/validate_login", methods = ["POST"])
def validateLogin():
    userName = request.form["username"]
    passWord = request.form["password"]
    user = User.query.filter_by(username = userName).first()
    
    if user:
        hashed_pw = user.hashPassword
        salt_pw = user.saltPassword
        if hashPassword(passWord, salt_pw.encode()) == (hashed_pw, salt_pw):
            session["user"] = user.username
            flash ("logged in as "+ session["user"])
            all_blogs = Blog.query.all()
            return render_template("allBlogs.html",all_blogs = all_blogs)
    return render_template("login.html", error_message= "invalid login information")   


#logout
@app.route("/logout")
def logout():
    del session["user"]
    flash ("you logged out")
    return redirect("/")


#default addForm
@app.route("/newPost")
def addPostDefault():
    return render_template("addPost.html")



#used to add individual posts after login
@app.route("/addPost", methods = ["POST"])
def addPost():
    if request.form["blogTitle"] and request.form["blogBody"]:
        title = request.form["blogTitle"]
        body = request.form["blogBody"]
        user = User.query.filter_by(username = session["user"]).first()

        new_blog = Blog(title, body, user)
        db.session.add(new_blog)
        db.session.commit()

        return render_template("newPost.html",pageTitle ="Blog Added Page", blogTitle = title, blogBody = body, record = new_blog.record )
    
    else:
        title_error = ""
        body_error= ""
        if not request.form["blogTitle"]:
            title_error = "Please provide a title"

        if not request.form["blogBody"]:
            body_error = "Please provide a body"

    return render_template("addPost.html",pageTitle ="Blog Added Page", title_error = title_error, body_error = body_error)
        
#show individual blog when link is clicked on
@app.route("/show")
def showPost():
    blogID = request.args.get("id")
    new_blog = Blog.query.filter_by(id = blogID).first()
    return render_template("newPost.html",pageTitle ="requested post", blogTitle = new_blog.title, blogBody = new_blog.body, record = new_blog.record )





#displays all posted blogs by user and is also the main page after login
@app.route("/main")
def displayAllPost():
    all_blogs = Blog.query.all()
    return render_template("allBlogs.html", all_blogs = all_blogs)



@app.route("/show_user")
def display_user():
    username = request.args.get("username")
    user = User.query.filter_by(username = username).first()
    return render_template ("allBlogs.html", all_blogs = user.blogs)












if __name__ == "__main__":
    app.run()


