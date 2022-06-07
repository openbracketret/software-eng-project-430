from django.shortcuts import render

from tools.viewsets import ActionAPIView


class ExternalScriptViewset(ActionAPIView):
    """
    The viewset class to handle requests from outside sources for adding scripts
    """

    