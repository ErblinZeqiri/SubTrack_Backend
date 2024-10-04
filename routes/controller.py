import os
import sys
from flask.views import MethodView
from flask_smorest import Blueprint
from flask import g, jsonify

sys.path.append(os.path.dirname(__file__))

# from .models import User, Subscription

from .dto.request.create import CreateUserRequest, CreateSubscriptionRequest, LoginRequest
from .dto.response.response import UserResponse, SubscriptionResponse, LoginResponse
from .dto.response.response_list import UserResponseList

from .service import UserService, SubscriptionService
from .mapper import UserMapper, SubscriptionMapper

from utils.jwt import create_token
from utils.decorators import authenticated
from flask_cors import cross_origin


# # # Users # # #
users = Blueprint("users", "users", url_prefix="/users", description="Users routes")
user_service = UserService()
user_mapper = UserMapper()

@users.route("/")
@authenticated
class UserController(MethodView):
  @users.arguments(CreateUserRequest)
  @users.response(status_code=201, schema=UserResponse)
  @users.response(status_code=422)
  def post(self, user: dict):
    try:
      return user_mapper.to_dict(user_service.create_user(user_mapper.to_user(user)))
    except ValueError as e:
      return {"message": str(e)}, 422
    

# # # Subscriptions # # #
subscriptions = Blueprint("subscriptions", "subscriptions", url_prefix="/subscriptions", description="Subscriptions routes")
subscription_service = SubscriptionService()
subscription_mapper = SubscriptionMapper()

@subscriptions.route("/")
class SubscriptionController(MethodView):
    @subscriptions.doc(description="Retrieve a list of subscriptions for the logged-in user")
    @subscriptions.response(status_code=200, description="Return the list of subscriptions for the user")
    @subscriptions.response(status_code=404, description="No subscriptions found")
    @authenticated
    def get(self):
        user_id = g.user_uid
        print(user_id)
        try:
            subscriptions = subscription_service.get_all(user_id)
            
            subscriptions_dict = [subscription_mapper.to_dict(sub) for sub in subscriptions]
            return jsonify(subscriptions_dict), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 404

    @subscriptions.arguments(CreateSubscriptionRequest)
    @subscriptions.response(status_code=201, schema=SubscriptionResponse)
    @subscriptions.response(status_code=422)
    @authenticated
    def post(self, subscription: dict):
        try:
            subscription["user_uid"] = g.user_uid
            return subscription_mapper.to_dict(subscription_service.create_subscription(subscription_mapper.to_subscription(subscription))), 201
        except ValueError as e:
            return {"message": str(e)}, 422
        
@subscriptions.route("/<subscription_id>", methods=["GET", "PUT", "DELETE"])
class SubscriptionController(MethodView):
    # Méthode GET pour récupérer une souscription par ID
    @subscriptions.doc(description="Retrieve a subscription by ID")
    @subscriptions.response(status_code=200, description="Return the subscription")
    @subscriptions.response(status_code=404, description="Subscription not found")
    @authenticated
    def get(self, subscription_id: str):
        try:
            subscription = subscription_service.get_one(subscription_id)
            return subscription_mapper.to_dict(subscription), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 404

    # Méthode PUT pour mettre à jour une souscription par ID
    @subscriptions.doc(description="Update a subscription by ID")
    @subscriptions.arguments(CreateSubscriptionRequest, location="json")  # Assure que les données sont dans le corps de la requête (JSON)
    @subscriptions.response(status_code=200, description="Subscription updated successfully")
    @subscriptions.response(status_code=404, description="Subscription not found")
    @authenticated
    def put(self, subscription_data: dict, subscription_id: str):  # `subscription_id` vient de l'URL, `subscription_data` du corps de la requête
        try:
            # Ajoute l'ID utilisateur et l'ID de la souscription mise à jour
            subscription_data["user_uid"] = g.user_uid
            subscription_data["id"] = subscription_id  # Associer l'ID de l'URL à la souscription
            subscription_service.update_subscription(subscription_mapper.to_subscription(subscription_data))
            return jsonify({"message": "Subscription updated successfully"}), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 404

    #Methode DELETE pour supprimer une souscription par ID
    @subscriptions.doc(description="Delete a subscription by ID")
    @subscriptions.response(status_code=200, description="Subscription deleted successfully")
    @subscriptions.response(status_code=404, description="Subscription not found")
    @authenticated
    def delete(self, subscription_id: str):
        try:
            subscription_service.delete_subscription(subscription_id)
            return jsonify({"message": "Subscription deleted successfully"}), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 404


# # # Login # # #
login = Blueprint("login", "login", url_prefix="/login", description="login routes")
@login.route("/", methods=["POST"])
@login.arguments(LoginRequest)
@login.response(status_code=200, schema=LoginResponse)
def login_with_email(login_request: LoginRequest):
    email = login_request['email']
    password = login_request['password']
    user = user_service.login(email, password)
    token = create_token(user.uid)
    return {"token": token}
  

logout = Blueprint("logout", "logout", url_prefix="/logout", description="logout routes")
@logout.route("/", methods=["POST"])
@authenticated
def logout_user():
    return {"message": "User logged out"}, 200


isAuthenticated = Blueprint("isAuthenticated", "isAuthenticated", url_prefix="/isAuthenticated", description="isAuthenticated routes")
@cross_origin(supports_credentials=True)
@isAuthenticated.route("/", methods=["GET"])
@authenticated
def is_Authenticated():
    return {"message": "User is authenticated"}, 200
