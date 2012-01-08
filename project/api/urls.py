from django.conf.urls.defaults import *

from piston.resource import Resource

from mealplanner.api.handlers import DishHandler, ListHandler, MealHandler, WeekHandler, DayHandler, EntryHandler

dish_handler = Resource(DishHandler)
meal_handler = Resource(MealHandler)
week_handler = Resource(WeekHandler)
list_handler = Resource(ListHandler)
day_handler = Resource(DayHandler)
entry_handler = Resource(EntryHandler)

urlpatterns = patterns('',
    url(r'^dishes/(?P<id>[\d]+)/', dish_handler),
    url(r'^dishes/', dish_handler),
    url(r'^meals/(?P<id>[\d]+)/', meal_handler),
    url(r'^meals/', meal_handler),
    url(r'^weeks/(?P<id>[\d]+)/', week_handler),
    url(r'^weeks/', week_handler),

    url(r'^days/(?P<id>[\d]+)/', day_handler),
    url(r'^days/', day_handler),

    url(r'^entries/(?P<id>[\d]+)/', entry_handler),
    url(r'^entries/', entry_handler),



    url(r'^lists/$',
        list_handler,
        ),

    url(r'^lists/(?P<model>(week|day|meal|dish))/(?P<slug>[-\w]+)/$',
        list_handler),

    url(r'^lists/(?P<model>(week|day|meal|dish))/$',
        list_handler),


)