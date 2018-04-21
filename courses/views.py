# from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateResponseMixin, View

from courses.forms import ModuleFormSet
from courses.models import Course, Subject


@login_required
def manage_course_list(request):
    """Vista basada en funcion que renderiza la lista de cursos guardados en la bd por usuario"""
    user = request.user
    queryset = Course.objects.filter(owner=user)
    return render(request, 'courses/manage/course/list.html', {'object_list': queryset})


class ManageCourseListView(ListView):
    """Vista basada en clase que renderiza la lista de cursos guardados en la bd por usuario"""
    model = Course
    template_name = 'courses/manage/course/list.html'

    def get_queryset(self):
        qs = super(ManageCourseListView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class CreateCourseView(CreateView):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    template_name = 'courses/manage/course/form.html'
    success_url = reverse_lazy("courses:manage_course_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CreateCourseView, self).form_valid(form)

    @method_decorator(permission_required('courses.add_course', reverse_lazy('courses:manage_course_list')))
    def dispatch(self, *args, **kwargs):
        return super(CreateCourseView, self).dispatch(*args, **kwargs)


class UpdateCourseView(UpdateView):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    template_name = 'courses/manage/course/form.html'
    success_url = reverse_lazy("courses:manage_course_list")

    @method_decorator(permission_required('courses.change_course', reverse_lazy('courses:manage_course_list')))
    def dispatch(self, *args, **kwargs):
        return super(UpdateCourseView, self).dispatch(*args, **kwargs)


class DeleteCourseView(DeleteView):
    model = Course
    success_url = reverse_lazy('courses:manage_course_list')
    template_name = 'courses/manage/course/delete.html'

    @method_decorator(permission_required('courses.delete_course', reverse_lazy('courses:manage_course_list')))
    def dispatch(self, *args, **kwargs):
        return super(DeleteCourseView, self).dispatch(*args, **kwargs)


# Course / Module


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs['pk']
        self.course = get_object_or_404(Course, id=pk, owner=self.request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:manage_course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})