from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import sqlite3

load_dotenv()  # loads variables from .env

app = Flask(__name__)
# session for password
app.secret_key = os.getenv('SECRET_KEY')

# Dynamic path configuration that adapts to both your local PC and PythonAnywhere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'messages.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'blog_images')

# database for contact form
def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# database table for blog posts
def init_blog_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blog_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            summary TEXT NOT NULL,
            content TEXT NOT NULL,
            date_posted TEXT NOT NULL,
            thumbnail TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_blog_db()

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
        (name, email, subject, message)
    )
    conn.commit()
    conn.close()

    return redirect('/contact.html?success=true')

@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

# rendering blogs from database
@app.route('/blog.html')
def blog():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blog_posts ORDER BY id DESC')
    posts = cursor.fetchall()
    conn.close()
    return render_template('blog.html', posts=posts)

@app.route('/certificates.html')
def certificates():
    return render_template('certificates.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/projects.html')
def projects():
    return render_template('projects.html')

@app.route('/resume.html')
def resume():
    return render_template('resume.html')

@app.route('/skills.html')
def skills():
    return render_template('skills.html')

# route to add new blog posts
@app.route('/add-blog', methods=['GET', 'POST'])
def add_blog():
    if request.method == 'POST':
        password = request.form.get('password')
        if password != os.getenv('ADMIN_PASSWORD'):
            return "Incorrect password", 401

        title = request.form.get('title')
        category = request.form.get('category')
        summary = request.form.get('summary')
        content = request.form.get('content')
        date_posted = datetime.now().strftime('%B %d, %Y')

        # Automatically create the image directory if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Handle thumbnail upload
        thumbnail_filename = None
        thumbnail_file = request.files.get('thumbnail')
        if thumbnail_file and thumbnail_file.filename:
            thumbnail_filename = secure_filename(thumbnail_file.filename)
            if thumbnail_filename:
                thumbnail_file.save(os.path.join(UPLOAD_FOLDER, thumbnail_filename))
            else:
                thumbnail_filename = None

        # Handle multiple content images
        content_images = request.files.getlist('content_images')
        for index, image_file in enumerate(content_images, start=1):
            if image_file and image_file.filename != '':
                safe_name = secure_filename(image_file.filename)
                image_file.save(os.path.join(UPLOAD_FOLDER, safe_name))
                placeholder = '{{image' + str(index) + '}}'
                image_html = f'<img src="/static/blog_images/{safe_name}" alt="Blog image {index}" style="width:100%; border-radius:8px; margin:20px 0;">'
                content = content.replace(placeholder, image_html)

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
       
        cursor.execute(
            'INSERT INTO blog_posts (title, category, summary, content, date_posted, thumbnail) VALUES (?, ?, ?, ?, ?, ?)',
            (title, category, summary, content, date_posted, thumbnail_filename)
        )
        conn.commit()
        conn.close()

        return redirect('/blog.html')

    return render_template('add_blog.html')

# blogs detail route to read blog
@app.route('/blog/<int:post_id>')
def blog_detail(post_id):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blog_posts WHERE id = ?', (post_id,))
    post = cursor.fetchone()
    conn.close()

    if post is None:
        return "Post not found", 404

    return render_template('blog_detail.html', post=post)

# log out add blog form
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/add-blog')

# delete route for blogs
@app.route('/delete-blog/<int:post_id>', methods=['GET', 'POST'])
def delete_blog(post_id):
    if request.method == 'POST':
        password = request.form.get('password')
        if password != os.getenv('ADMIN_PASSWORD'):
            return "Incorrect password", 401

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM blog_posts WHERE id = ?', (post_id,))
        conn.commit()
        conn.close()

        return redirect('/blog.html')

    return render_template('delete_blog.html', post_id=post_id)

# manage blogs(delete)
@app.route('/manage-blog', methods=['GET', 'POST'])
def manage_blog():
    if request.method == 'POST':
        password = request.form.get('password')
        if password != os.getenv('ADMIN_PASSWORD'):
            return "Incorrect password", 401

        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM blog_posts ORDER BY id DESC')
        posts = cursor.fetchall()
        conn.close()

        return render_template('manage_blog.html', posts=posts, password=password)

    return render_template('login.html', action='/manage-blog')

# view contact form messages
@app.route('/view_messages', methods=['GET', 'POST'])
def view_messages():
    if request.method == 'POST':
        password = request.form.get('password')
        if password != os.getenv('ADMIN_PASSWORD'):
            return "Incorrect password", 401

        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM messages ORDER BY id DESC')
        messages = cursor.fetchall()

        unread_count = sum(1 for msg in messages if msg['is_read'] == 0)

        # Mark all as read now that you've viewed them
        cursor.execute('UPDATE messages SET is_read = 1')
        conn.commit()
        conn.close()

        return render_template('view_messages.html', messages=messages, password=password, unread_count=unread_count)

    return render_template('login.html', action='/view_messages')

# route for delete messages (contact form)
@app.route('/delete-message/<int:msg_id>', methods=['POST'])
def delete_message(msg_id):
    password = request.form.get('password')
    if password != os.getenv('ADMIN_PASSWORD'):
        return "Incorrect password", 401

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM messages WHERE id = ?', (msg_id,))
    conn.commit()
    conn.close()
    return redirect('/view_messages')

if __name__ == '__main__':
    app.run(debug=True)
