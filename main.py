from flask import Flask
from flask import render_template

app = Flask(__name__, static_url_path='/static')

@app.route('/hello/')
def hello_world():
  return 'Hello, World!'


@app.route('/')
# @app.route('/hello/<name>')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
  app.run()
