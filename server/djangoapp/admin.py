from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 0

# CarMakeAdmin class
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

# CarModelAdmin class with CarModelInline
class CarModelAdmin(admin.ModelAdmin):
    list_filter = ['name']

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)