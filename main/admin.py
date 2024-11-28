from django.contrib import admin
from .models import Momo,Touch
# Register your models here.
admin.site.register(Touch)
@admin.register(Momo)
class MomoAdmin(admin.ModelAdmin):
    list_display=['id','category','price','title','image']
