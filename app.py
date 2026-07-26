from flask import Flask

# Flask specifically looks for this variable named 'app'
app = Flask(__name__)

@app.route('/')
def home():
    return "Flask backend is running successfully!"

if __name__ == '__main__':
    app.run(debug=True)
