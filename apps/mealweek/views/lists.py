from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.core import serializers
from django.utils import simplejson
from django.views.generic.simple import direct_to_template
from django.db.models.query import QuerySet

from itertools import chain

from meal.models import Meal, Dish, CustomIngredient
from mealweek.models import Week, Day

def list_detail (request, model, slug, api=False):
    object_type = model
    try:
        #isn't there a python or django way to do this differently?
        #MUST CHANGE THIS - this usage of EVAL is BAD.
        #Only security check for this is:
        #(?P<model>(week|day|meal|dish) in url conf
        model = eval(model.title())
    except NameError:
        raise Http404

    obj = get_object_or_404(model, slug=slug)
    

    meals = False

    if model is Week:
        ingredients = Ingredient.objects.filter(dish__meal__entry__day__week=obj)
        custom_ingredients = CustomIngredient.objects.filter(dish__meal__entry__day__week=obj)
        meals = Meal.objects.filter(entry__day__week=obj).distinct()
    if model is Day:
        ingredients = Ingredient.objects.filter(dish__meal__entry__day__id=obj.id)
        custom_ingredients = CustomIngredient.objects.filter(dish__meal__entry__day__id=obj.id)
        meals = Meal.objects.filter(entry__day__id=obj.id).distinct()
    if model is Meal:
        ingredients = Ingredient.objects.filter(dish__meal=obj)
        custom_ingredients = CustomIngredient.objects.filter(dish__meal=obj)
    if model is Dish:
        ingredients = Ingredient.objects.filter(dish=obj)
        custom_ingredients = CustomIngredient.objects.filter(dish=obj)


    all_ingredients = {}
    for ingredient in chain(ingredients, custom_ingredients):
        if type(ingredient) is Ingredient:
            is_ingredient = True
            prefix = "ingredient_"
        else:
            is_ingredient = False
            prefix = "customingredient_"

        if not all_ingredients.get(prefix + str(ingredient.id)):
            if is_ingredient:
                name = ingredient.shrt_desc
            else:
                name = ingredient.name
            all_ingredients[prefix + str(ingredient.id)]={'name': name}

#    list_data = {'all_ingredients': all_ingredients,
#                 'obj': obj,
#                 'object_type': object_type,
#                 'meals': meals,
#                 }

    
    list_data = {'items': [{'name': "turkey salad",
                             'leaf': False,
                             'ingredients': [{'name': "turkey",
                                              'leaf': True,
                                            },
                                             {'name': "lettuce",
                                              'leaf': True,
                                             }
                                            ]

                             },
                             {'name': "salmon souflee",
                             'leaf': True,
                             'ingredients': []
                             }
                 ]}

    if api:
        json_data = simplejson.dumps(list_data, indent=4, default=encode_model_objects)
        return HttpResponse(json_data,  mimetype='application/json; charset=utf-8')
    else:
        return direct_to_template(request, template='lists/list_detail.html',
                                  extra_context=list_data,
                        )

def list_list(request, model, api=False):
    object_type = model
    try:
        #isn't there a python or django way to do this differently?
        #MUST CHANGE THIS - this usage of EVAL is BAD.
        #Only security check for this is:
        #(?P<model>(week|day|meal|dish) in url conf
        model = eval(model.title())
    except NameError:
        raise Http404

    object_list = model.objects.all()


    list_data = {'object_list': object_list,
                'object_type': object_type,
                }

    if api:
        json_data = simplejson.dumps([list_data], indent=4, default=encode_model_objects)
        return HttpResponse(json_data,  mimetype='application/json; charset=utf-8')
    else:
        return direct_to_template(request, template='lists/list_list.html',
                                       extra_context=list_data,
                             )


def list_list_top_level(request, api=False):

    if api:
        pass
    else:
        return direct_to_template(request,
                                  template='lists/list_list_top_level.html')



def encode_model_objects(obj):
    if isinstance(obj, Day):
        return {
            "id": obj.id,
            "name": obj.name,
            "type": obj.type,
            #obj.date
            }
    elif isinstance(obj, Week):
        return {
            "id": obj.id,
            "name": obj.name,
            #obj.date
            }
    elif isinstance(obj, Meal):
        return {
            "id": obj.id,
            "name": obj.name,
            #obj.date
            }
    elif isinstance(obj, Dish):
        return {
            "id": obj.id,
            "name": obj.name,
            #obj.date
            }
    elif isinstance(obj, QuerySet):
        if isinstance(obj[0], Meal):
            objects = []
            for object in obj:
                objects.append({"name": object.name,
                                "id": object.id,
                                })
            return objects
        elif isinstance(obj[0], Dish):
            objects = []
            for object in obj:
                objects.append({"name": object.name,
                                "id": object.id,
                                })
            return objects
        elif isinstance(obj[0], Week):
            objects = []
            for object in obj:
                objects.append({"name": object.name,
                                "id": object.id,
                                })
            return objects
        elif isinstance(obj[0], Day):
            objects = []
            for object in obj:
                objects.append({"name": object.name,
                                "id": object.id,
                                })
            return objects
    else:
        raise TypeError(repr(obj) + " is not JSON serializable")