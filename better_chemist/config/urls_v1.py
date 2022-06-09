from django.urls import path, include, re_path

from script.views import  ExternalScriptViewset, ScriptViewset

urlpatterns = [
    # Our /v1/* urls go here
    re_path(r'^external_actions/(?P<action>[^/.]+)', ExternalScriptViewset.as_view(), name='external-script'),
    re_path(r'^script_actions/(?P<action>[^/.]+)', ScriptViewset.as_view(), name='internal-script'),
]

# /admin_actions/projects?id=1