from django.shortcuts import render

from script.serializers import ScriptBaseSerializer

from tools.viewsets import ActionAPIView


class ExternalScriptViewset(ActionAPIView):
    """
    The viewset class to handle requests from outside sources for adding scripts
    """

    def post_upload_script(self, request, params, *args, **kwargs):

        data = {
            'file': params['file'],
            'created_by_id': request.user.id,
            'max_redeems': params['max_redeems'],
        }

        serializer = ScriptBaseSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return "Script Uploaded"

        return {
            "success": False,
            "payload": {
                "error": serializer.errors
            }
        }

