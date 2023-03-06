from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Cat, Toy, Photo

from .forms import FeedingForm
import uuid
import boto3


# temporary cats for building templates
# views.py
# Add this cats list below the imports
# cats = [
#   {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
#   {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
#   {'name': 'Tubs', 'breed': 'ragdoll', 'description': 'little and chunky', 'age': 0},
# ]


# Create your views here.

# define our home view function

# view funcs match urls to code, like controllers in express

def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

# about route
def about(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'about.html')

# Add new view
def cats_index(request):
  # We pass data to a template very much like we did in Express!
  # gather relations using models
  cats = Cat.objects.all()
  return render(request, 'cats/index.html', {
    'cats': cats
  })

def cats_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)

  #get list of ids of toys cat owns
  id_list = cat.toys.all().values_list('id')
  toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)

  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form' : feeding_form, 'toys': toys_cat_doesnt_have })

class CatCreate(CreateView):
  model = Cat
  fields = '__all__'
  # success_url = '/cats/{cat_id}'

class CatUpdate(UpdateView):
  model = Cat
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
  model = Cat
  success_url = '/cats'

def add_feeding(request, cat_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('detail', cat_id=cat_id)

def assoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.add(toy_id)
  return redirect('detail', cat_id=cat_id)

def unassoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.remove(toy_id)
  return redirect('detail', cat_id=cat_id)

# toylist
class ToyList(ListView):
  model = Toy
  template_name = 'toys/index.html'


# toydetail

class ToyDetail(DetailView):
  model = Toy
  template_name = 'toys/detail.html'

# toycreate

class ToyCreate(CreateView):
  model = Toy
  fields = ['name', 'color']

  # define inherited method is_valid does
  def form_valid(self, form):
    return super().form_valid(form)
  
# toyupdate

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

# toydelete
class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'