from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env

app = Flask(__name__)


# for contact form submission
import sqlite3

# database for contact form
def init_db():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# data base table for blog posts
def init_blog_db():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blog_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            summary TEXT NOT NULL,
            content TEXT NOT NULL,
            date_posted TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_blog_db()
    



from flask import request, redirect

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    conn = sqlite3.connect('messages.db')
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

#rendering blogs from database
@app.route('/blog.html')
def blog():
    conn = sqlite3.connect('messages.db')
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
        title = request.form.get('title')
        category = request.form.get('category')
        summary = request.form.get('summary')
        content = request.form.get('content')
        date_posted = request.form.get('date_posted')

        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO blog_posts (title, category, summary, content, date_posted) VALUES (?, ?, ?, ?, ?)',
            (title, category, summary, content, date_posted)
        )
        conn.commit()
        conn.close()

        return redirect('/blog.html')

    return render_template('add_blog.html')



# blogs detail route to read blog
@app.route('/blog/<int:post_id>')
def blog_detail(post_id):
    conn = sqlite3.connect('messages.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blog_posts WHERE id = ?', (post_id,))
    post = cursor.fetchone()
    conn.close()

    if post is None:
        return "Post not found", 404

    return render_template('blog_detail.html', post=post)




if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')