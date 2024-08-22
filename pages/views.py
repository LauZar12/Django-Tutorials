from django.http import HttpResponseRedirect
from django.shortcuts import render # here by default
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
class HomePageView(TemplateView):
 template_name = 'pages/home.html'

class AboutPageView(TemplateView):
 template_name='pages/about.html'
 def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Laura Danniela Zárate Guerrero.",
        })
        return context

class ContactPageView(TemplateView):
 template_name='pages/contact.html'
 def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact - Online Store",
            "subtitle": "Contact",
            "mail": "lauralaura@gmail.com",
            "phone": "3333333333",
            "address": "Calle 1 #2-3",
            "author": "Developed by: Laura Danniela Zárate Guerrero.",
        })
        return context


class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 500.00},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 999.00},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 35.00},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 150.00}
    ]


class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}
        if int(id) - 1 > len(Product.products):
            return HttpResponseRedirect(reverse("home"))
        product = Product.products[int(id) - 1]
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)


class ProductFormView(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductFormView()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProductFormView(request.POST)
        if form.is_valid():
            new_product = {
                "id": str(len(Product.products) + 1),
                "name": form.cleaned_data['name'],
                "price": form.cleaned_data['price'],
                "description": "Default Description",
            }
            Product.products.append(new_product)
            #messages.success(request, "Product created")
            return redirect('success')
        return render(request, self.template_name, {'form': form})

class ProductSuccessView(View):
    template_name = 'products/success.html'
    def get(self, request):
        viewData = {}
        return render(request, self.template_name)


