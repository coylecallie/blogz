from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:hello123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blogpost')
def blog_post():
    id = int(request.args.get('id'))
    blog = Blog.query.filter_by(id=id).first()
    return render_template('blog_post.html', id=id, blog=blog)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html')

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']

        blog_title_error == ''
        blog_body_error == ''

        if blog_title == "":
            blog_title_error = "You need to submit a title for your blog post, please"

        if blog_body == "":
            blog_body_error = "You need to submit content for your blog post, please"

        if blog_body_error or blog_title_error:
            return render_template('new_post.html', blog_title=blog_title, blog_body=blog_body)
        
        else:
            blog = Blog(blog_title, blog_body)
            db.session.add(blog)
            db.session.commit()
            return render_template('blog_post.html', blog=blog, blog_title=blog_title, blog_body=blog_body)

if __name__ == '__main__':
    app.run()
