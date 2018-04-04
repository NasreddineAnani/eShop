from flask import Flask, render_template, flash, redirect, url_for, session, logging
from data import getData
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

app = Flask(__name__)

articles = getData()

# Index
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/produits')
def products():
    return render_template('products.html', Articles=articles)


@app.route('/products/<string:id>/')
def article(id):
    return render_template('article.html', id=id)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])


if __name__ == '__main__':
    app.run(debug=True)
