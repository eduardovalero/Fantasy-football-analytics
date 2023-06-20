from flask import Flask, render_template

app = Flask(__name__)

# Root route
@app.route('/')
def home():
    return "Welcome to my Flask web app!"

# Run as script
if __name__ == '__main__':
    app.run()