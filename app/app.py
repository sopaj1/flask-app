from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import mysql.connector
from typing import List, Dict
from mysql.connector import Error


app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = '../static/uploads'
# Enssure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'posts'
        }

# Memory for blog posts (Replace with DB later)
blog_posts = []

@app.route('/')
def index():
    return render_template('index.html')

def get_posts() -> list[Dict]:
    print('GETTING POSTS')
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('SELECT title, date, story FROM blog_posts')
        result = cursor.fetchall()
        print(result)
        results = [{'title': title, 'date': date, 'story': story} for (title, date, story) in result]
        cursor.close()
        connection.close()
        print(f'Results {results}')
        return results
    except Error as e:
        return None


@app.route('/blog', methods=["GET", "POST"])
def blog():
    print('BLOG LOADED')
    c = get_posts()
    if c is None:
        return render_template('blog.html', blog_posts=[{"title": "Database Failed to load", "story": "Looking into it"}])

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
        #ADD LATER
        # image = request.files['images']
        # if image:
        #     filename = secure_filename(image.filename)
        #     image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     post['image'] = filename

        # add blog post here and refresh page
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO blog_posts (title, date, story) VALUES (%s, %s, %s)',
                       (title, date, story))
        connection.commit()
        cursor.close()
        connection.close()
        # blog_posts.append(post)  # Change for DB later
        return redirect(url_for('blog')) # redirect to blog page
    
    posts = get_posts()
    # update list from DB
    return render_template('blog.html', blog_posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")  # debug=True for development.  Don't use in production!