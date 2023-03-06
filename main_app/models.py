from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.

# A tuple of 2-tuples
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)
# new code above
class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.color} {self.name}'
    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id})

class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)

    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

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
      # change the default sort
    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for cat_id: {self.cat_id} @{self.url}"
