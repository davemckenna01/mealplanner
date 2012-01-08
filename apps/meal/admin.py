from django.contrib import admin

from meal.models import Dish, Meal

#class IngredientAdmin(admin.ModelAdmin):
#    pass

class DishAdmin(admin.ModelAdmin):
    pass

class MealAdmin(admin.ModelAdmin):
    filter_horizontal = ('dishes',)
    pass



#admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Meal, MealAdmin)