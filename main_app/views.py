from django.shortcuts import render

# temporary cats for building templates
# views.py
# Add this cats list below the imports
cats = [
  {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
  {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
  {'name': 'Tubs', 'breed': 'ragdoll', 'description': 'little and chunky', 'age': 0},
]


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
  return render(request, 'cats/index.html', {
    'cats': cats
  })
