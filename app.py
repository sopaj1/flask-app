from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename

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

@app.route('/blog', methods=["GET", "POST"])
def blog():
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
        blog_posts.append(post)  # Change for DB later

        return redirect(url_for('blog')) # redirect to blog page
    return render_template('blog.html', blog_posts=blog_posts)


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)  # debug=True for development.  Don't use in production!