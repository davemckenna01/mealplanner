from django import forms

from meal.models import Dish, Meal, CustomIngredient, DishCustomIngredient

class DishForm(forms.ModelForm):

    class Meta:
        model = Dish

    def save(self):
        """
        Need to override save() because of the intermediary models used for
        Dish -> Ingredient, and Dish -> CustomIngredient relationships.
        The OOTB save() on ModelForms does not support intermediary models.
        """

        custom_ingredients = self.data.getlist('custom_ingredients')

        dish = self.instance

        if dish.id:
            if custom_ingredients:
                dishcustomingredients = DishCustomIngredient.objects.filter(dish=dish)
                for dci in dishcustomingredients:
                    if unicode(dci.custom_ingredient_id) not in custom_ingredients:
                        dci.delete()

        dish.save()

        if custom_ingredients:
            dishcustomingredients = DishCustomIngredient.objects.filter(dish=dish)
            dci_ids = [unicode(dci.custom_ingredient_id) for dci in dishcustomingredients]
            for i in custom_ingredients:
                if unicode(i) not in dci_ids:
                    custom_ingredient = CustomIngredient.objects.get(pk = i)
                    DishCustomIngredient.objects.create(dish = dish, custom_ingredient = custom_ingredient)

        return dish

        
class MealForm(forms.ModelForm):

    class Meta:
        model = Meal


class CustomIngredientForm(forms.ModelForm):

    class Meta:
        model = CustomIngredient
