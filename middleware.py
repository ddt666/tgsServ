from django.middleware.security import SecurityMiddleware

from django.utils.deprecation import MiddlewareMixin


class MyCore(MiddlewareMixin):
    def process_response(self, request, response):

        # print(request.environ['HTTP_ORIGIN'])
        # response["Access-Control-Allow-Origin"] = request.environ['HTTP_ORIGIN']
        response["Access-Control-Allow-Origin"] = '*'
        # response[" Access-Control-Allow-Headers"] = ["POST"]
        # response["Access-Control-Allow-Credentials"] = "true"

        return response
