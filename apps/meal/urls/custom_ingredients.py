from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object

from meal.models import CustomIngredient
from meal.forms import CustomIngredientForm

urlpatterns = patterns('',


                        url(r'^$',
                            object_list,
                            { 'queryset': CustomIngredient.objects.all(),
                               'paginate_by': 20 },
                            name='meal_custom_ingredient_list'),

                        url(r'^(?P<object_id>\d+)/$',
                            object_detail,
                            { 'queryset': CustomIngredient.objects.all()},
                            name='meal_custom_ingredient_detail'),

                        url(r'^create/$',
                            create_object,
                            { 'form_class': CustomIngredientForm,
                              'extra_context': {'operation': 'create'},
                            },
                            name='meal_custom_ingredient_create'),

                        url(r'^update/(?P<object_id>\d+)/$',
                            update_object,
                            { 'form_class': CustomIngredientForm,
                              'extra_context': {'operation': 'update'},
                            },
                            name='meal_custom_ingredient_update'),

                        url(r'^delete/(?P<object_id>\d+)/$',
                            delete_object,
                            { 'model': CustomIngredient,
                              'post_delete_redirect': '/meal/custom_ingredients/',
                            },
                            name='meal_custom_ingredient_delete'),




)