from django.shortcuts import render, redirect
from login.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from login.models import Noticia
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def index_view(request):

	if request.method=='POST':
		#form=LoginForm(request.POST)
		username=request.POST['username']
		password=request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			# the password verified for the user
			if user.is_active:
				login(request, user)
				return redirect("/")
			else:
				return redirect("/inactivo")
		else:
			# the authentication system was unable to verify the username and password
			return redirect("/")
	else:
		form=LoginForm()
		return render(request, 'login.html', {'form': form})


def salir(request):

	logout(request)
	return redirect("/")


class MuestraNoticia(DetailView):

	model = Noticia
	template_name = 'noticia.html'
	slug_field = 'id'


class MuestraTodasNoticias(ListView):

    model = Noticia
    template_name = 'noticias.html'
    slug_field = 'id'
    paginate_by = 2

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(MuestraTodasNoticias, self).dispatch(*args, **kwargs)


class CreaNoticia(CreateView):
    model = Noticia
    template_name = 'noticiaAdd.html'
    fields = ['title', 'description']
    success_url = '/list/'

class ActualizaNoticia(UpdateView):
    model = Noticia
    template_name = 'noticiaAdd.html'
    fields = ['title', 'description']
    success_url = '/list/'

class BorraNoticia(DeleteView):
    model = Noticia
    template_name = 'noticiaDelete.html'
    #success_url = reverse_lazy('author-list')
    success_url = '/list/'
