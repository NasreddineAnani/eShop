from flask import Flask, render_template
from data import articles

app = Flask(__name__)

articles = articles()

# Index
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/products')
def products():
    return render_template('products.html', Articles = articles)

if __name__ == '__main__':
	app.run(debug=True)
