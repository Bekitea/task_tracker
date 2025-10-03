from django.core.exceptions import PermissionDenied, ValidationError
from django.http import JsonResponse


class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            return JsonResponse(
                {'error': str(exception)},
                status=403
            )

        elif isinstance(exception, ValidationError):
            if hasattr(exception, 'message_dict'):
                errors = exception.message_dict
            elif hasattr(exception, 'messages'):
                errors = list(exception.messages)
            else:
                errors = str(exception)

            return JsonResponse(
                {'error': errors},
                status=400
            )

        return JsonResponse(
            {'error': 'Внутренняя ошибка сервера'},
            status=500
        )
