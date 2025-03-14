from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Post, Comment

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
    if not session.get('user'):
        return redirect(url_for('login'))
    posts = Post.query.all()  # Lấy lại dữ liệu từ database
    return render_template('index.html', posts=posts, user=session.get('user'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, role='user')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

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

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if not session.get('user'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user = User.query.get(session['user']['id'])
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        if check_password_hash(user.password, old_password):
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
            db.session.commit()
            return redirect(url_for('dashboard'))
    return render_template('change_password.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('user'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_url = request.form['image_url']
        new_post = Post(title=title, content=content, image_url=image_url)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('dashboard'))

    posts = Post.query.all()
    users = User.query.all()
    return render_template('dashboard.html', posts=posts, users=users, user=session.get('user'))



@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if not session.get('user'):
        return redirect(url_for('login'))

    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if not session.get('user'):
        return redirect(url_for('login'))

    content = request.form['content']
    new_comment = Comment(post_id=post_id, user_id=session['user']['id'], content=content)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('home'))
@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    if not session.get('user') or session['user']['role'] != 'actor':
        return redirect(url_for('home'))

    comment = Comment.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
