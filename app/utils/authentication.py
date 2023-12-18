from functools import wraps
from flask import request
from app.utils.http_response import HttpResponse
from dynaconf import settings
import jwt


def authentication(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        try:
            if "Authorization" in request.headers:

                token = str(request.headers["Authorization"]).replace("Bearer ", "")
                res = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

            else:
                return HttpResponse("error", "Unauthorized", 401).http_response()

        except Exception as error:
            return HttpResponse("error", error.args[0], 403).http_response()


        return f(*args, **kwargs)
    return wrapper


def decode_user():

    try:
        if "Authorization" in request.headers:

            token = str(request.headers["Authorization"]).replace("Bearer ", "")
            return jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            
    except Exception:
        return None