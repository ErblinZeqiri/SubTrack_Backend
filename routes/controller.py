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
def logout():
    return {"message": "User logged out"}, 200

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
            subscription["user_uid"] = g.user_uid,
            return subscription_mapper.to_dict(subscription_service.create_subscription(subscription_mapper.to_subscription(subscription)))
        except ValueError as e:
            return {"message": str(e)}, 422
