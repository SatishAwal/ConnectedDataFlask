from flask import Flask, render_template

app = Flask(__name__) # Changed 'app' to __name__ as is standard practice

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__': # Added this block for better practice
    app.run(host='0.0.0.0', port=8080)