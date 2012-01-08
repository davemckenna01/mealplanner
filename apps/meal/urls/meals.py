from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object

from meal.models import Meal
from meal.forms import MealForm

urlpatterns = patterns('',


                        url(r'^$',
                            object_list,
                            { 'queryset': Meal.objects.all(),
                               'paginate_by': 20 },
                            name='meal_meal_list'),

                        url(r'^create/$',
                            create_object,
                            { 'form_class': MealForm,
                              'extra_context': {'operation': 'create'},
                            },
                            name='meal_meal_create'),

                        url(r'^update/(?P<slug>[-\w]+)/$',
                            update_object,
                            { 'form_class': MealForm,
                              'extra_context': {'operation': 'update'},
                            },
                            name='meal_meal_update'),

                        url(r'^delete/(?P<slug>[-\w]+)/$',
                            delete_object,
                            { 'model': Meal,
                              'post_delete_redirect': '/meal/meals/',
                            },
                            name='meal_meal_delete'),

                        url(r'^(?P<slug>[-\w]+)/$',
                            object_detail,
                            { 'queryset': Meal.objects.all()},
                            name='meal_meal_detail'),


)