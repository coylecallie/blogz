from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'Y2M3C1A4'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')


    def __init__(self, username, password):
        self.username = username 
        self.password = password


@app.before_request
def require_login():
    require_login = ['new_post']
    if request.endpoint in require_login and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    users = User.query.all()
    
    return render_template('index.html', title="blog users!", users=users)

@app.route('/blog')
def blog():
    blogs = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('blog.html', title="blog posts!", blogs=blogs)


@app.route('/blog_post')
def blog_post():
    blog_id = request.args.get('id')
    blog = Blog.query.get(blog_id)
    return render_template('blog_post.html', blog=blog, blog_id=blog_id)

@app.route('/singleUser')
def singleUser():
    user_id = request.args.get('id')
    blogs = Blog.query.filter_by(owner_id=user_id).all()
    return render_template('singleUser.html', user_blogs=blogs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("LOGGED IN WOOO!!!!!")
            return redirect('/newpost')
        else:
            flash("PASSWORD IS WRONG OR USER DOES NOT EXIST YET","error") 
    return render_template('login.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST': 
        username = request.form['username'] 
       
        if len(username) < 3 or len(username) > 20 or ' ' in username:
            flash("WRONG, USERNMANE MUST BE BETWEEN 3 AND 20 CHARACTERS WITH NO SPACES!!!", "error")
            return redirect('/signup')

        password = request.form['password'] 
        verify = request.form['verify']

        if len(password) < 3 or len(password) > 20 or ' ' in password:
            flash("WRONG, PASSWORD MUST BE BETWEEN 3 AND 20 CHARACTERS WITH NO SPACES!!!", "error")
            return redirect ('/signup')

        if verify != password or len(verify) == 0:
            flash("PASSWORDS DO NOT MATCH< TRY AGAIN!!!", "error")
            return redirect ('/signup')

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash("GOOD JOB< YOU REGISTERED")
            return redirect('/newpost')
        else:
            flash('USER EXISTS ALREADY DUDE', 'error')    
    return render_template('signup.html')


@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html', title="Add a Blog Entry")

    owner = User.query.filter_by(username=session['username']).first()   
    owner_id = owner.id

    if request.method == 'POST':
        title = request.form['blog_title']
        blog_body = request.form['blog_body']
        
        if title == "":
            flash("YOU NEED A TITLE!!!","error")
            return redirect('/newpost')

        if blog_body == "":
            flash("YOU NEED CONTENT!!!","error")
            return redirect('newpost')
            
        else: 
            newpost = Blog(title, blog_body, owner)
            db.session.add(newpost)
            db.session.commit()
            blog = Blog.query.filter_by(title=title).first()
            user = User.query.filter_by(id = owner_id).first()
            return redirect('/blog_post?id={id}'.format(id = blog.id))


@app.route('/logout', methods=['GET'])
def logout():
    if "username" in session:
        del session["username"]
    return redirect('/login')
        

if __name__ == '__main__':
    app.run()

