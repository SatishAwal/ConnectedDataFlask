from flask import Flask, render_template

app = Flask(__name__) # Changed 'app' to __name__ as is standard practice

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/about')
@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact')
@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/projects')
@app.route('/projects.html')
def projects():
    return render_template('projects.html')

@app.route('/Weather')
@app.route('/Weather.html')
def weather():
    return render_template('Weather.html')

@app.route('/blog')
@app.route('/blog.html')
def blog():
    return render_template('blog.html')

if __name__ == '__main__': # Added this block for better practice
    app.run(host='0.0.0.0', port=8080)

