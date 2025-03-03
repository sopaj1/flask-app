from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import mysql.connector

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
# Enssure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Memory for blog posts (Replace with DB later)
blog_posts = []

@app.route('/')
def index():
    return render_template('index.html')
    
def get_db_connection():
    try:
        return mysql.connector.connect(
            user='root',
            password='root',
            host='db',
            port='3306',
            database='posts'
        )
    except:
        print(f"Error with database")
        return None

@app.route('/blog', methods=["GET", "POST"])
def blog():
    connection = get_db_connection()
    if connection is None:
        return render_template('blog.html', blog_posts=[{"title": "Database Failed to load", "story": "Looking into it"}])
    cursor = connection.cursor()

    if request.method == 'POST':
        title = request.form['title']
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        story = request.form['story']
        post = {
            'title': title,
            'date': date,
            'story': story,
        }
        image = request.files['images']
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            post['image'] = filename
        # add blog post here and refresh page
        cursor.execute('INSERT INTO blog_posts (title, date, story, image) VALUES (%s, %s, %s, %s)',
                       (title, date, story, filename))
        connection.commit()

        # blog_posts.append(post)  # Change for DB later
        return redirect(url_for('blog')) # redirect to blog page
    
    cursor.execute('SELECT title, date, story, image FROM blog_posts ORDER BY date DESC')
    posts = [{"title": title, "date": date, "story": story, "image": image} for (title, date, story, image) in cursor]
    
    cursor.close()
    connection.close()
    # update list from DB
    return render_template('blog.html', blog_posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()  # debug=True for development.  Don't use in production!