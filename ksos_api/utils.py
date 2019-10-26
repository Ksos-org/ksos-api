import random
import string
from datetime import timedelta, datetime, date

from django.core.cache import cache
from rest_framework.response import Response

from api.enums import PickerPeriodType


class Utils:
    @staticmethod
    def is_get(request):
        return Utils.__check_request_type(request, 'GET')

    @staticmethod
    def is_post(request):
        return Utils.__check_request_type(request, 'POST')

    @staticmethod
    def is_put(request):
        return Utils.__check_request_type(request, 'PUT')

    @staticmethod
    def is_patch(request):
        return Utils.__check_request_type(request, 'PATCH')

    @staticmethod
    def is_delete(request):
        return Utils.__check_request_type(request, 'DELETE')

    @staticmethod
    def __check_request_type(request, method):
        return request.method == method

    @staticmethod
    def error_response(errors, status, headers=None):
        return Response({'errors': errors}, status=status, headers=headers)

    @staticmethod
    def error_response_with_message(message, errors, status, headers=None):
        return Response({'message': message, 'errors': errors}, status=status, headers=headers)

    @staticmethod
    def execute_sql_script(script):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(script)
            fetch_result = cursor.fetchall()
        return fetch_result
