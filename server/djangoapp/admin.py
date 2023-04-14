from django.contrib import admin
# from .models import related models


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
from .models import CarMake, CarModel

class CarModelInline(admin.StackedInline):

    list_display = ['name',  'dealer_id', 'car_type', 'year']
    model = CarModel
    extra = 5

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [
        CarModelInline,
    ]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)