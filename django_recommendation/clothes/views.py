from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User
from .models import Cloth
from .forms import ClothCreationForm


class HomePageView(TemplateView):
    template_name = 'index.html'


class SignUpView(CreateView):
    model = User
    template_name = 'user_creation_form.html'
    fields = ['username', 'password']


class ClothCreationView(CreateView):
    model = Cloth
    template_name = 'product_creation_form.html'
    fields = ['name', 'price', 'image']
    success_url = 'home'
    form_class = ClothCreationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect(self.success_url)
        else:
            print(form)
            return render(request, self.template_name, {'form': form})

def create_product(request):
    if request.method == 'POST':
        form = ClothCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/success/url/')
        else:
            print(form.__dict__)
            print(request.FILES)
    else:
        form = ClothCreationForm()
    return render(request, 'product_creation_form.html', {'form': form})
