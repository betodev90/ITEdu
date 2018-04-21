# Importamos la vista genérica FormView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
# Importamos la libreria de authorizacion de django
from django.contrib.auth import login
from django.http.response import HttpResponseRedirect

from .forms import FormLogin


class Login(FormView):
    # Establecemos el template a utilizar
    template_name = 'security/login.html'
    # Le indicamos que el formulario a utilizar es el formulario de autenticación de Django
    form_class = FormLogin
    # Le decimos que cuando se haya completado exitosamente la operación nos redireccione a la url bienvenida de
    # la aplicación personas
    success_url = reverse_lazy("inicio")

    def dispatch(self, request, *args, **kwargs):
        # Si el usuario está autenticado entonces nos direcciona a la url establecida en success_url
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        # Sino lo está entonces nos muestra la plantilla del login simplemente
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)