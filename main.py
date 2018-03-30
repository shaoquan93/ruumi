from flask import Flask
from flask import render_template

app = Flask(__name__, static_url_path='/static')

@app.route('/shop/')
# @app.route('/hello/<name>')
def shop():
    return render_template('shop.html')

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/guest/')
def guest_index():
    return render_template('guest_index.html')

@app.route('/space123/')
def space123():
    return render_template('single.html')

@app.route('/checkout/', methods=['GET', 'POST'])
def checkout():
    return render_template('checkout.html')

@app.route('/done/', methods=['GET', 'POST'])
def done():
    return render_template('done.html')

@app.route('/host/')
def host_index():
    return render_template('host_index.html')

@app.route('/myacc/')
def account():
    return render_template('myacc.html')

@app.route('/myspaces/')
def myspaces():
    return render_template('myplaces.html')

@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/space123calendar/')
def calendar():
    return render_template('calendar.html', sub=True)

if __name__ == '__main__':
  app.run()
