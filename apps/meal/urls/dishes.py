from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object


from meal.models import Dish
from meal.forms import DishForm
from meal.views.dishes import *

urlpatterns = patterns('',


                        url(r'^$',
                            object_list,
                            { 'queryset': Dish.objects.all(),
                               'paginate_by': 20 },
                            name='meal_dish_list'),

                        url(r'^create/$',
                            create_object,
                            { 'form_class': DishForm,
                              'extra_context': {'operation': 'create'},
                            },
                            name='meal_dish_create'),

                        url(r'^update/(?P<slug>[-\w]+)/$',
                            update_object,
                            { 'form_class': DishForm,
                              'extra_context': {'operation': 'update'},
                            },
                            name='meal_dish_update'),

                        url(r'^delete/(?P<slug>[-\w]+)/$',
                            delete_object,
                            { 'model': Dish,
                              'post_delete_redirect': '/meal/dishes/',
                            },
                            name='meal_dish_delete'),

                        url(r'^(?P<slug>[-\w]+)/$',
                            object_detail,
                            { 'queryset': Dish.objects.all()},
                            name='meal_dish_detail'),


)
