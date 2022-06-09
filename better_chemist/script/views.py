from argparse import Action
from django.shortcuts import render
from yaml import serialize

from script.serializers import ScriptBaseSerializer, CustomerBaseSerializer
from script.models import Customer, Script, ScriptRedeems

from tools.viewsets import ActionAPIView


class ExternalScriptViewset(ActionAPIView):
    """
    The viewset class to handle requests from outside sources for adding scripts
    """

    def post_upload_script(self, request, params, *args, **kwargs):

        print(request.user.id)
        data = {
            'file': params.get('file', None),
            'created_by': request.user.id,
            'max_redeems': params.get('max_redeems', None),
            'customer_id_number': params.get('customer_id_number', None)
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

        serializer = CustomerBaseSerializer(customer)

        return serializer.data

    def post_add_customer(self, request, params, *args, **kwargs):

        data = {
            "id_number": params.get("id_number", None),
            "contact_number": params.get("contact_number", None),
            "first_name": params.get("first_name", None),
            "surname": params.get("surname", None),
            "address": params.get("address", None)
        }

        serializer = CustomerBaseSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return "Customer added"
        
        return {
            "success": False,
            "payload": serializer.errors
        }

    def post_redeem_script(self, request, params, *args, **kwargs):

        if not params.get("customer_id", None):
            return {
                "success": False,
                "message": "Please provide customer id"
            }

        if not params.get("script_id", None):
            return {
                "success": False,
                "message": "Please provide script id"
            }

        try:
            script = Script.objects.get(id=params['script_id'])
        except Script.DoesNotExist:
            return {
                "success": False,
                "message": "No script with that ID exists"
            }

        try:
            customer = Customer.objects.get(id=params['customer_id'])
        except Customer.DoesNotExist:
            return {
                "success": False,
                "message": "No customer with that ID exists"
            }

        redeemed_count = ScriptRedeems.objects.filter(script=script, customer=customer).count()

        if redeemed_count >= script.max_redeems:
            return {
                "success": False,
                "message": "The selected script has been redeemed the max amount of times already"
            }

        ScriptRedeems.objects.create(
            script=script,
            customer=customer
        )

        return "Script redeemed"
        
    def post_check_for_existing_script(self, request, params, *args, **kwargs):

        if not params.get("id_number", None):
            return {
                "success": False,
                "message": "Please provide an id number"
            }

        scripts = Script.objects.filter(customer_id_number=params['id_number'])

        if not scripts.exists():
            return {
                "success": False,
                "message": "No scripts with that customer id number"
            }

        script = scripts.latest('id')

        serializer = ScriptBaseSerializer(script)
        return serializer.data


    def post_add_new_script(self, request, params, *args, **kwargs):

        data = {
            "file": params.get("file", None),
            "created_by": request.user.id,
            "max_redeems": params.get("max_redeems", None),
            "customer_id_number": params.get("customer_id_number", None)
        }

        serializer = ScriptBaseSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return serializer.data

        return {
            "success": False,
            "payload": serializer.errors
        } 