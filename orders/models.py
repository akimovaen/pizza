from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.formats import localize

# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=20)
    image = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.name}"


class Items(models.Model):
    TRAITS = (
        ('S', 'Small'),
        ('L', 'Large'),
        ('A', 'Addition'),
    )
    
    name = models.CharField(max_length=30)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu")
    trait = models.CharField(max_length=1, choices=TRAITS, null=True, blank=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.menu} - {self.name} ({self.get_trait_display()})"

    def is_valid_trait(self):
        t = self.trait
        return (t == 'S') or (t == 'L') or (t == 'A') or (t == None)

    def save(self, *args, **kwargs):
        valid_trait = self.is_valid_trait()
        if valid_trait ==False:
            message = "Trait must be 'Small', 'Large', 'Addition' or None"
            raise ValidationError(message)

        super().save(*args, **kwargs)


class Order(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('C', 'Complete'),
    )

    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="person")
    number = models.IntegerField()
    placing_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS, default="P")
    complete_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.status == "P":
            return f"Order N{self.number} placing {localize(self.placing_time)} ({self.get_status_display()})"
        else:
            return f"Order N{self.number} placing {localize(self.placing_time)} ({self.get_status_display()}  {localize(self.complete_time)})"


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    dish = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="dish")
    add1 = models.ForeignKey(Items, on_delete=models.CASCADE, null=True, blank=True, related_name="add1")
    add2 = models.ForeignKey(Items, on_delete=models.CASCADE, null=True, blank=True, related_name="add2")
    add3 = models.ForeignKey(Items, on_delete=models.CASCADE, null=True, blank=True, related_name="add3")
    ordered = models.BooleanField(default=False)
    order_number = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name="order_number")

    def cart_view(self):
        if not self.dish.trait:
            self.dish.trait = ""
        view = {
            "id": self.id,
            "menu": self.dish.menu.name,
            "name": self.dish.name,
            "size": self.dish.get_trait_display(),
            "price": self.dish.price
        }
        
        if self.add1:
            if self.add1.price:
                view["add1"] = {"name": self.add1.name, "price": self.add1.price}
            else:
                view["add1"] = {"name": self.add1.name, "price": ""}
        if self.add2:
            if self.add2.price:
                view["add2"] = {"name": self.add2.name, "price": self.add2.price}
            else:
                view["add2"] = {"name": self.add2.name, "price": ""}
        if self.add3:
            if self.add3.price:
                view["add3"] = {"name": self.add3.name, "price": self.add3.price}
            else:
                view["add3"] = {"name": self.add3.name, "price": ""}
        return view

    def __str__(self):
        if self.ordered:
            return f"Order N{self.order_number.number}"
        else:
            return "Not ordered"