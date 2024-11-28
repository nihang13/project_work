from django.db import models

# Create your models here.
class Touch(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.IntegerField()
    message=models.TextField()

choice_field=(
    ('buff','buff'),
    ('veg','veg'),
    ('chicken','chicken')
)
class Momo(models.Model):
    category=models.CharField(choices=choice_field,max_length=200)
    title=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    image=models.ImageField(upload_to="images") #pip install pillow
    