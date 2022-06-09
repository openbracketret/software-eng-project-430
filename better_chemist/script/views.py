from argparse import Action
from django.shortcuts import render

from script.serializers import ScriptBaseSerializer, CustomerBaseSerializer
from script.models import Customer, Script, ScriptRedeems

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


class ScriptViewset(ActionAPIView):
    """
    The viewset used to manage everything internal to do with scripts
    """

    def get_search_customer(self, request, params, *args, **kwargs):

        if params.get("id_number", None):
            try:
                customer = Customer.objects.get(id_number=params['id_number'])
            except Customer.DoesNotExist:
                return {
                    "success": False,
                    "message": "No customer with that ID number exists"
                }
        else:
            return {
                "success": False,
                "message": "Please provide an ID number to search by"
            }

        serializer = CustomerBaseSerializer(data=customer)

        return serializer.data