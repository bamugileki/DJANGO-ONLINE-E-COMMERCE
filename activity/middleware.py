from .utils import log_activity


class ActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            path = request.path
            if '/dashboard/' in path or '/admin/' in path:
                action = 'delete' if request.method == 'DELETE' else ('create' if 'add' in path else 'update')
                log_activity(
                    request, action,
                    description=f'{request.method} {path}',
                )
        return None
