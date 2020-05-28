from django.db import models

# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"


class Items(models.Model):
    TRAITS = (
        ('S', 'Small'),
        ('L', 'Large'),
        ('A', 'Addition')
    )
    
    name = models.CharField(max_length=30)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu")
    trait = models.CharField(max_length=1, choices=TRAITS, null=True, blank=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.menu} - {self.name} ({self.trait})"
