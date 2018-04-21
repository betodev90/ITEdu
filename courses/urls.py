from django.conf.urls import url
from .views import *

urlpatterns = [
    # url(r'^$', manage_course_list, name='manage_course_list')
    url(r'^$', ManageCourseListView.as_view(), name='manage_course_list'),
    url(r'^nuevo/$', CreateCourseView.as_view(), name='course_create'),
    url(r'^(?P<pk>\d+)/editar/$', UpdateCourseView.as_view(), name='course_edit'),
    url(r'^(?P<pk>\d+)/eliminar/$', DeleteCourseView.as_view(), name='course_delete'),

    # Module
    url(r'^(?P<pk>\d+)/modulo/$', CourseModuleUpdateView.as_view(), name='course_module_update'),
]
