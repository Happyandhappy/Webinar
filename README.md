Webinar_Flask
===========

The purpose of this project is to build a landing page for a webinar and a checkout page for users that purchase. This is a template that can be easily changed and I am using the code in the folder '05-rotating-text' for the landing page. The form uses PHP but I would like to build a flask backend and then use javascript for submitting the form so that we do not have to do a page refresh.

We will also need to implement the themes checkout form with the Stripe API.


Requirements
------------

- Flask (`pip install flask`).
- Stripe (`pip install stripe`).
- Airtable (`pip install airtable-python-wrapper`).

Installation
------------

You can create a virtual environment and install the required packages with the following commands:

    $ virtualenv venv
    $ . venv/bin/activate
    (venv) $ pip install -r requirements.txt

Setting of config.py
--------------------
	create config.py file and add following code	

	SUB_URL = "http://sendy.XXX.com/subscribe"
	LIST_ID = "XXXX"   ( sendy list id )
	API_KEY = "XXXX"   ( Airtable api key )
	BASE_ID = "XXXX"   ( Airtable base/app ID)
	STRIPE_PUB_KEY="XXXX"  ( Stripe Publick Key )
	STRIPE_SEC_KEY = "XXXX"  ( Stripe secret Key )

Running the Flask app
--------------------

With the virtual environment activated you can `cd` into any of the examples and run the main script.

Running :

    (venv) $ python flaskapp.py



