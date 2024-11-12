
class DatabaseRoutingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check request path and set a flag or context variable indicating the database
        if request.path.startswith('/ontario/'):
            request.use_database = 'Ontario'
        # elif request.path.startswith('/database2/'):
        #     request.use_database = 'database2'
        else:
            request.use_database = 'default'
        
        response = self.get_response(request)
        return response