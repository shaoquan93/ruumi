from flask import Flask
from flask import render_template

app = Flask(__name__, static_url_path='/static')

@app.route('/hello/')
def hello_world():
  return 'Hello, World!'

@app.route('/shop/')
# @app.route('/hello/<name>')
def shop():
    return render_template('shop.html')


@app.route('/')
# @app.route('/hello/<name>')
def hello():
    return render_template('index.html')

@app.route('/space123/')
# @app.route('/hello/<name>')
def new():
    return render_template('single.html')

if __name__ == '__main__':
  app.run()
