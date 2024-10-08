from flask import request, jsonify, g, make_response
from functools import wraps
from .jwt import decode_token

def authenticated(func):
  @wraps(func)
  def token_verification(*args, **kwargs):
    token = None
    if 'Authorization' in request.headers:
      try:
        typ, token = request.headers["Authorization"].split()
        if typ != "Bearer":
          raise ValueError
      except ValueError:
        return {"error": "Invalid token format, must be: Bearer <token>"}, 401
    if token == None:
      return {"error": "Token is missing"}, 401
    try:
      g.userID = decode_token(token)
    except Exception as e:
      return jsonify({"error": str(e)}), 401  
    return func(*args, **kwargs)
  return token_verification

def handle_cors_options(func):
  def decorator(*args, **kwargs):
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:4200")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        response.headers.add('Access-Control-Allow-Credentials', "true")
        return response
    return func(*args, **kwargs)
  return decorator