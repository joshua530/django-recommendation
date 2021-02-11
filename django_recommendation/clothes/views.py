from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.models import User
from .models import Cloth, Opinion, Purchase
from .forms import ClothCreationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.http import HttpResponse

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')

def product_opinion(request):
    # had to print this out for the request to finally go through
    # print(request.COOKIES)
    response = {'errors': None, 'liked': 'false', 'disliked': 'false'}
    if not request.user.is_authenticated:
        # user not authenticated
        response['errors'] = 'Ensure you are logged in before attempting to like or dislike an item'
        return HttpResponse(json.dumps(response), content_type='application/json')

    user = request.user
    action = request.POST['action']
    product_id = request.POST['product-id']

    product = Cloth.objects.filter(id=product_id)
    if request.method == 'POST':
        # product being given an opinion on exists and opinion is valid
        if len(product) == 1 and (action == 'like' or action == 'dislike'):
            product = product[0]
            opinion = Opinion.objects.filter(user=user, product=product)
            if len(opinion) != 0:
                # get saved opinion
                opinion_id = opinion[0].id
                opinion_name = opinion[0].name
                opinion = Opinion(id=opinion_id, name=opinion_name, user=user, product=product)
                if opinion.name == action:
                    # reverting previous opinion eg hit like button after liking product previously
                    # meaning user wants to unlike the product
                    opinion.name = None
                else:
                    opinion.name=action
            else:
                # create new opinion
                opinion = Opinion(name=action, product=product, user=user)
            opinion.save()
        else:
            response['errors'] = 'Sorry, an error occured, please refresh your browser and try again'
    # fetch the product opinions as they are
    opinion = Opinion.objects.filter(user=user, product=product)
    if len(opinion) > 0:
        opinion = opinion[0]
        opinion_type = opinion.name
        if opinion_type == 'like':
            response['liked'] = 'true'
        elif opinion_type == 'dislike':
            response['disliked'] = 'true'
    return HttpResponse(json.dumps(response), content_type='application/json')



class HomePageView(ListView):
    template_name = 'index.html'
    context_object_name = 'clothes'

    def get_login_url(self):
        messages.info(self.request, 'Login to continue')
        return reverse('login')

    def get_queryset(self):
        queryset = Cloth.objects.all()

        for cloth in queryset:
            cloth.opinion = None
            cloth.purchased = False
            if self.request.user.is_authenticated:
                opinion = Opinion.objects.filter(product=cloth, user=self.request.user)
                if len(opinion) != 0:
                    cloth.opinion = opinion[0].name
                purchase = Purchase.objects.filter(product=cloth, user=self.request.user)
                if (len(purchase) != 0):
                    cloth.purchased = True

        return queryset

class LoginView(TemplateView):
    template_name = 'login_form.html'

    def post(self, *args, **kwargs):
        request = self.request
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
        return render(request, template_name='login_form.html')

class SignUpView(CreateView):
    model = User
    template_name = 'user_creation_form.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('home')


class ClothCreationView(LoginRequiredMixin, CreateView):
    model = Cloth
    template_name = 'product_creation_form.html'
    fields = ['name', 'price', 'image']

    def get_success_url(self):
        return reverse('home')

class ProductPurchaseView(LoginRequiredMixin, CreateView):
    def post(self, *args, **kwargs):
        request = self.request
        product_id = request.POST['product-id']
        product = Cloth.objects.filter(id=product_id)
        if (len(product) == 0):
            return redirect('home')
        product = product[0]
        user = request.user
        purchase = Purchase.objects.filter(user=user, product=product)

        if len(purchase) != 0:
            return redirect('home')
        purchase = Purchase(user=user, product=product)
        purchase.save()

        return redirect('home')
