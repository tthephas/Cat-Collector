from django.db import models
from django.urls import reverse

# Create your models here.

# A tuple of 2-tuples
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)
# new code above


class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

# dunder method str
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat_id': self.id })
    
# Add new Feeding model below Cat model
class Feeding(models.Model):
    date = models.DateField('Feeding date')
    meal = models.CharField(
        max_length=1,
        choices = MEALS,
        default = MEALS[0][0]
    )
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    def __str__(self):
    
        return f"{self.get_meal_display()} on {self.date}"