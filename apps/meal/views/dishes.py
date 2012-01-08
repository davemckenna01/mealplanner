from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from meal.models import Dish, DishCustomIngredient


def measurements(request, slug):
    if request.method == "POST":
        error = False

        for ingredient in request.POST:
            if len(request.POST[ingredient]) <= 100:
                i = DishCustomIngredient.objects.get(pk=ingredient.replace("dci_", ""))

                i.measurement=request.POST[ingredient]
                i.save()
            else:
                error = True


        if not error:
            return HttpResponseRedirect(reverse('meal_dish_detail', kwargs={'slug': slug }))


    elif request.method == "GET":
        error = False

    
    dish = get_object_or_404(Dish, slug=slug)
    dishcustomingredients = DishCustomIngredient.objects.filter(dish=dish)

    response = render_to_response ("meal/dish_detail_measurements.html",
                                   {
                                    'dishcustomingredient_list': dishcustomingredients,
                                    'dish': dish ,
                                    'error': error,
                                   }
                                   )
    
    return response