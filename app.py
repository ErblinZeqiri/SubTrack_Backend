from flask import Flask
from flask_smorest import Api
from flask_cors import CORS

from routes.controller import users, subscriptions, login, isAuthenticated

server = Flask(__name__)

class APIConfig:
  API_TITLE = "SubTrack Backend API"
  API_VERSION = "v1"  
  OPENAPI_VERSION = "3.0.2"
  OPENAPI_URL_PREFIX = "/"
  OPENAPI_SWAGGER_UI_PATH = "/docs"
  OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


server.config.from_object(APIConfig)
CORS(server, supports_credentials=True)


api = Api(server)
api.register_blueprint(users)
api.register_blueprint(subscriptions)
api.register_blueprint(login)
api.register_blueprint(isAuthenticated)

if __name__ == "__main__":
  server.run(debug=True, port=5050, host='0.0.0.0')