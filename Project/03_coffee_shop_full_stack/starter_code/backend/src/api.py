import os
import sys, traceback
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()
setup_db(app)
CORS(app, resources={r"/*":{"origins":"*"}})

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods","GET,POST,PATCH,DELETE,OPTIONS")
    response.headers.add("Access-Control-Allow-Credentials","true")
    return response

'''
Uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
#db_drop_and_create_all()

# ROUTES
@app.route('/drinks')
def get_drinks():
    drinks_query = Drink.query.all()
    try:
        drinks = [drink.short() for drink in drinks_query]
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except:
        etype, value, tb = sys.exc_info()
        print(traceback.print_exception(etype, value, tb))
        abort(404)

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    print(payload)
    drinks_query = Drink.query.all()
    try:
        drinks = [drink.long() for drink in drinks_query]

        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except:
        etype, value, tb = sys.exc_info()
        print(traceback.print_exception(etype, value, tb))
        abort(404)

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    body = request.get_json()
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)

    try:
        drink = Drink(title=new_title,recipe=json.dumps(new_recipe))
        if Drink.query.filter_by(title=drink.title).count() < 1:
            drink.insert()

        return jsonify({
            "success": True,
            "drinks": json.dumps([drink.long()])
        }), 200
    except:
        etype, value, tb = sys.exc_info()
        print(traceback.print_exception(etype, value, tb))
        abort(422)

@app.route('/drinks/<int:id>',methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload,id):
    body = request.get_json()
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404)
        drink.title = body.get('title')
        #drink.recipe = body.get('recipe')
        drink.update()

        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })
    except:
        etype, value, tb = sys.exc_info()
        print(traceback.print_exception(etype, value, tb))
        abort(422)

@app.route('/drinks/<int:id>', methods=['DELETE','GET'])
@requires_auth('delete:drinks')
def delete_drink(payload,id):
    print(payload)
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    print(drink)
    if drink is None:
        abort(404)
    try:
        drink.delete()
        return jsonify({
            "success": True,
            "delete": id
        }), 200
    except:
        etype, value, tb = sys.exc_info()
        print(traceback.print_exception(etype, value, tb))
        abort(422)

# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
