"""
    Flask Backend for Webinar.
    User Registeration & Stripe Checkout
    2/19/2019
"""

from flask import Flask, render_template, request
import requests
import stripe
from config import *

app = Flask(__name__)
stripe.api_key = STRIPE_SEC_KEY

## validate form data with mane array
def validate(names, form):
    var = {}
    message = None
    for name in names:
        if name in form and form[name] != 'undefined':
            var.update({name : form[name]})
        else:
            message = "% is required" % (name.capitalize())
    return var, message

## add subscriber to list of sendy
def subscribe(data):
    res = requests.post(SUB_URL, data=data)
    if res.text == '1':
        return "success"
    else:
        return res.text

## route for Landing page
@app.route('/')
def index():
    return render_template('index.html')

## route for registeration process
@app.route('/registration', methods=['POST'])
def registration():
    names = ['firstname', 'lastname','email','terms']
    data, message = validate(names, request.form)
    if message:
        return message
    postdata = {
        "name": data['firstname'] + " " + data['lastname'],
        "email": data['email'],
        "list": LIST_ID,
        "boolean": "true"
    }
    return subscribe(postdata)


@app.route('/deletesubscriber', methods=['POST'])
def delete():
    if 'email' in request.form:
        email = request.form['email']
    else:
        return "Email is required"

    postdata = {
        "api_key" : API_KEY,
        "list_id" : LIST_ID,
        "email"   : email
    }

    res = requests.post("http://sendy.pythonfinancial.com/api/subscribers/delete.php", data=postdata)
    return res.text if res.text != '1' else 'success'

## route for Contact form
@app.route('/contact', methods=['POST'])
def contact():
    names = ['name','email','message']
    data, message = validate(names, request.form)
    if message:
        return message
    postdata = {
        "name": data['name'],
        "email": data['email'],
        "list": LIST_ID,
        "boolean": "true"
    }
    return subscribe(postdata)

## route for Payment
@app.route('/payment')
def payment():
    return render_template('payment.html', stripe_key=STRIPE_PUB_KEY)

## route for Payment Checkout
@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 9900
    names = ['firstname', 'lastname', 'phone','email','terms','stripeToken']
    data, message = validate(names, request.form)
    if message:
        return message
    email = data['email']
    token = data['stripeToken']

    customer = stripe.Customer.create(
        email=email,
        source=token
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Argo Training Course'
    )
    return 'success'

if __name__ == '__main__':
    app.run(debug=True)