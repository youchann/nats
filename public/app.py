from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello():
    name = "Hello World"
    return render_template('hello.html')

## おまじない
if __name__ == "__main__":
    app.run()
