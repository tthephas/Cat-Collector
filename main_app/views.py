from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Cat, Toy, Photo

from .forms import FeedingForm
import uuid
import boto3
from django.conf import settings


# Add the two imports below
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin



AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
S3_BUCKET = settings.S3_BUCKET
S3_BASE_URL = settings.S3_BASE_URL

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
@login_required
def cats_index(request):
  # We pass data to a template very much like we did in Express!
  # gather relations using models
  # cats = Cat.objects.all()
  cats = Cat.objects.filter(user=request.user)
  return render(request, 'cats/index.html', {
    'cats': cats
  })

@login_required
def cats_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)

  #get list of ids of toys cat owns
  id_list = cat.toys.all().values_list('id')
  toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)

  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form' : feeding_form, 'toys': toys_cat_doesnt_have })

class CatCreate(LoginRequiredMixin, CreateView):
  model = Cat
  # fields = '__all__'
  fields = ['name', 'breed', 'description', 'age']
  # success_url = '/cats/{cat_id}'
  # This inherited method is called when a
  # valid cat form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
  model = Cat
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['breed', 'description', 'age']

class CatDelete(LoginRequiredMixin, DeleteView):
  model = Cat
  success_url = '/cats'

@login_required
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

@login_required
def assoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.add(toy_id)
  return redirect('detail', cat_id=cat_id)

@login_required
def unassoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.remove(toy_id)
  return redirect('detail', cat_id=cat_id)

# toylist
class ToyList(LoginRequiredMixin, ListView):
  model = Toy
  template_name = 'toys/index.html'


# toydetail

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy
  template_name = 'toys/detail.html'

# toycreate

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = ['name', 'color']

  # define inherited method is_valid does
  def form_valid(self, form):
    return super().form_valid(form)
  
# toyupdate

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

# toydelete
class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

@login_required
def add_photo(request, cat_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            # bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, S3_BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{S3_BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, cat_id=cat_id)
            # Photo.objects.create(url=url, cat_id=cat_id)
            photo.save()
        except Exception as error:
            print('An error occurred uploading file to S3')
            print(error)
            return redirect('detail', cat_id=cat_id)
    return redirect('detail', cat_id=cat_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
