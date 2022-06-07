from django.urls import path, include, re_path

from script.views import  ExternalScriptViewset

urlpatterns = [
    # Our /v1/* urls go here

    # re_path(r'^test_actions/(?P<action>[^/.]+)', TestViewSet.as_view(), name='test'),
    re_path(r'^external_actions/(?P<action>[^/.]+)', ExternalScriptViewset.as_view(), name='external-script'),
    # re_path(r'^student_actions/(?P<action>[^/.]+)', ProjectStudentViewSet.as_view(), name='project-student'),
    # path('projects', ProjectViewSet.as_view(
    #     {
    #         'get': 'get_projects'
    #     }
    # ), name='project-list'),
    # path('projects', ProjectAdminViewSet.as_view({
    #     'get': 'list'
    # }), name='project-admin')

]

# /admin_actions/projects?id=1