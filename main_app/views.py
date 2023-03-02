from django.shortcuts import render

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