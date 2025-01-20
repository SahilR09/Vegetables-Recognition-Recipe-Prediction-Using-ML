from django.db import models
from django.contrib.auth.models import User

class FavouriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=255)
    ingredients = models.TextField()
    prep_time = models.CharField(max_length=50)
    cook_time = models.CharField(max_length=50)
    cuisine = models.CharField(max_length=100)
    instructions = models.TextField()

    def __str__(self):
        return f"{self.recipe_name} - {self.user.username}"
