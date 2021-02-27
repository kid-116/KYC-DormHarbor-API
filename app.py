from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask import make_response


import os
from silasdk import App
from silasdk import User
from silasdk import Transaction
silaApp=App("SANDBOX","4bf733034c47a00f1fb5096e88d1ccccff919cc714cbfaa3896db66c72e5898f","kyc-dormharbor")


app = Flask(__name__)
api = Api(app)


class check_handle(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument("handle", required=True)
    params = parser.parse_args()
    payload = {
      "user_handle": params["handle"]
    }
    response = User.checkHandle(silaApp, payload)
    if response["status_code"] == 200:
        return response["message"], 200
    else:
        return response["message"], 400

class register(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument("country", required=True)
    parser.add_argument("user_handle", required=True)
    parser.add_argument("first_name", required=True)
    parser.add_argument("last_name", required=True)
    parser.add_argument("entity_name", required=True)
    parser.add_argument("identity_value", required=True)
    parser.add_argument("phone", type=int, required=True)
    parser.add_argument("email", required=True)
    parser.add_argument("street_address_1", required=True)
    parser.add_argument("city", required=True)
    parser.add_argument("state", required=True)
    parser.add_argument("postal_code", type=int, required=True)
    parser.add_argument("crypto_address", required=True)
    parser.add_argument("birthdate", required=True)
    payload = parser.parse_args()
    payload["phone"] = int(payload["phone"])
    payload["postal_code"] = int(payload["postal_code"])
    response = User.register(silaApp, payload)
    if response["status_code"] == 200:
        return response["message"], 200
    else:
        return response["message"], 400
    
class request_kyc(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument("user_handle", required=True)
    parser.add_argument("user_private_key", required=True)
    params = parser.parse_args()
    payload = {
      "user_handle": params["user_handle"]
    }
    response = User.requestKyc(silaApp, payload, params["user_private_key"], use_kyc_level=False)
    if response["status_code"] == 200:
        return response["message"], 200
    else:
        return response["message"], 400

class check_kyc(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument("user_handle", required=True)
    parser.add_argument("user_private_key", required=True)
    params = parser.parse_args()
    payload = {
      "user_handle": params["user_handle"]
    }
    response = User.checkKyc(silaApp,payload, params["user_private_key"])
    if response["status_code"] == 200:
        return response["message"], 200
    else:
        return response["message"], 400

api.add_resource(check_handle, "/check-handle", "/check-handle/")
api.add_resource(register, "/register", "/register/")
api.add_resource(request_kyc, "/request-kyc", "/request-kyc/")
api.add_resource(check_kyc, "/check-kyc", "/check-kyc/")