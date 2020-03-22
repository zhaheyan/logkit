
def get_request_args(func):
    def _get_request_args(self, request):
        if request.method == 'GET':
            args = request.GET
        else:
            # body = request.body
            body = request.data
            if body:
                try:
                    # args = json.loads(body)
                    args = body
                except Exception as e:
                    LOG.error(e)
                    # return makeJsonResponse(status=StatusCode.EXECUTE_FAIL, message=str(e))
                    args = request.POST
            else:
                args = request.POST
        return func(self, request, args)

    return _get_request_args

