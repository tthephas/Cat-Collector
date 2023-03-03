from django.contrib import admin

# import your models here
from .models import Cat, Feeding, Toy

# Register your models here
admin.site.register(Cat)

# register the new Feeding Model 
admin.site.register(Feeding)


admin.site.register(Toy)

