"""
    Flask Backend for Webinar.
    User Registeration & Stripe Checkout
    2/19/2019
"""

from flask import Flask, render_template, request
import requests
import stripe
import os
from airtable import Airtable

app = Flask(__name__)
stripe.api_key = STRIPE_SEC_KEY
at = Airtable(base_key=BASE_ID, table_name='Users', api_key=API_KEY)

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
    fields = {
        "Name"  : data['name'],
        "Phone" : data['phone'],
        "Email" : data['email'],
        "Tags"  : [data['tags']]
    }

    ## for first registration , check email existance in table
    if data['tags'] == "Registered Preview":
        res = at.search('Email', data['email'])
        if len(res) > 0:
            return "Email Already Registered!"
        at.insert(fields)
    else:
    ## for Payment case, update the status of Tags
        at.update_by_field('Email', data['email'], fields)
    return "success"


## route for Landing page
@app.route('/')
def index():
    return render_template('index.html')

## route for Thank you page
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

## route for registeration process
@app.route('/registration', methods=['POST'])
def registration():
    names = ['firstname', 'lastname','email','terms']
    data, message = validate(names, request.form)
    if message:
        return message
    # register to Airtable
    return subscribe({
        "name"  : data['firstname'] + " " + data['lastname'],
        "email" : data['email'],
        "phone" : '',
        "tags"  : "Registered Preview"
    })

## route for Contact form
@app.route('/contact', methods=['POST'])
def contact():
    names = ['name','email','message']
    data, message = validate(names, request.form)
    if message:
        return message

    return subscribe({
        "name": data['name'],
        "email": data['email'],
        "list": LIST_ID,
        "boolean": "true"
    })

## route for Payment
@app.route('/payment')
def payment():
    return render_template('payment.html', stripe_key=STRIPE_PUB_KEY)

## route for Payment Checkout
@app.route('/charge', methods=['POST'])
def charge():
    amount = 9900
    names = ['firstname', 'lastname', 'phone','email','terms','stripeToken']
    data, message = validate(names, request.form)
    if message:
        return message
    email = data['email']
    token = data['stripeToken']

    ## check email was registered in Registration page
    res = at.search('Email', data['email'])
    if len(res) == 0:
        return "Email was not registered!"
    elif 'Registered Basic' in res[0]['fields']['Tags']:
        return "Already purchased"

    ## Transaction process in Stripe
    try:
        customer = stripe.Customer.create( email=email, source=token)
        stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='RE Cash Infusion'
        )
    except:
        return 'Problem with the card'

    return subscribe({
        "name"  : data['firstname'] + " " + data['lastname'],
        "email" : data['email'],
        "phone" : data['phone'],
        "tags"  : "Registered Basic"
    })

if __name__ == '__main__':
    app.run(debug=True)
