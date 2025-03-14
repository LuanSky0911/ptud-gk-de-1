from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, backref
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'user' hoặc 'actor'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Post {self.title}>"
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    post = db.relationship('Post', backref=db.backref('comments', lazy=True))
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

with app.app_context():
    db.create_all()
    if User.query.count() == 0:
        admin = User(username='admin', password=generate_password_hash('admin123', method='pbkdf2:sha256'), role='actor')
        db.session.add(admin)
        db.session.commit()
    if Post.query.count() == 0:
        sample_posts = [
            Post(title="Bài viết 1", content="Nội dung bài viết 1", image_url="https://picsum.photos/800/400"),
            Post(title="Bài viết 2", content="Nội dung bài viết 2", image_url="https://picsum.photos/800/400"),
            Post(title="Bài viết 3", content="Nội dung bài viết 3", image_url="https://picsum.photos/800/400")
        ]
        db.session.bulk_save_objects(sample_posts)
        db.session.commit()

@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=posts, user=session.get('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = {'id': user.id, 'username': user.username, 'role': user.role}
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if not session.get('user') or session['user']['role'] != 'actor':
        return redirect(url_for('home'))
    posts = Post.query.all()
    return render_template('dashboard.html', posts=posts, user=session.get('user'))


if __name__ == '__main__':
    app.run(debug=True)
