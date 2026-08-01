from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username


class Recipe(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.TextField()
    recipe_image = models.ImageField(upload_to='recipes/', blank=True, null=True)

    def __str__(self):
        return self.name

    def total_cost(self):
        return sum(i.cost or 0 for i in self.ingredients.all())


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=200)
    quantity = models.FloatField()
    unit_price = models.FloatField()
    cost = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.cost = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.recipe.name})"