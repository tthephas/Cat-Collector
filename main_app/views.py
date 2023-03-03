from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Cat

from .forms import FeedingForm


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
  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form' : feeding_form })

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

