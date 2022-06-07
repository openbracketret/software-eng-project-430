from django.http import QueryDict, HttpResponse, StreamingHttpResponse

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from tools.serializer import APISerializer

class ActionAPIView(APIView):
    """
    Utility class to make setting up routing within the application just a little easier for everyone.
    The class will route URLs to functions based on their names.
    Simple, really.
    """

    permission_classes = [permissions.IsAuthenticated]
    _last_action = None
    success = True
    RESPONSE_KEYS = []
    raw_body = ''

    def get(self, request, action, **kwargs):
        return self.handle_request(request, action, "get", **kwargs)

    def post(self, request, action, **kwargs):
        return self.handle_request(request, action, "post", **kwargs)
        

    def handle_request(self, request, action, request_type, **kwargs):
        params = self.normalize_params(request)
        kwargs['params'] = params

        self._last_action = params.get('action', action)

        try:
            lv_action = self.__getattribute__(f'{request_type}_{self._last_action}')
        except AttributeError:
            return Response({"success": False, "reason": "Invalid action"})
        response = lv_action(request, **kwargs)
        if isinstance(response, Response):
            response = response.data
        if isinstance(response, (HttpResponse, StreamingHttpResponse)):
            return response

        response_context = dict(
            [item for item in list({
                k: params.get(k, None) for k in self.RESPONSE_KEYS
            }.items()) if item[1] is not None]
        )
        serialized = APISerializer(response, context=response_context)
        return Response(serialized.data)


    def normalize_params(self, request):
        try:
            self.raw_body = request._request.body
        except:
            self.raw_body = ''
        
        params = request.query_params.dict().copy()
        if isinstance(request.data, QueryDict):
            params.update(request.data.dict())
        else:
            params.update(request.data)
        return params
