from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from mealplanner.views import login

from settings import PROJECT_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, { 'template': 'static/homepage.html',
                                  #'name': "homepage",
                                }),

    (r'^ingredients/', include('meal.urls.custom_ingredients')),
    (r'^dishes/', include('meal.urls.dishes')),
    (r'^meals/', include('meal.urls.meals')),

    (r'^schedule/weeks/', include('mealweek.urls.weeks')),
    (r'^schedule/days/', include('mealweek.urls.days')),

    (r'^lists/', include('mealweek.urls.lists')),

    (r'^api/', include('mealplanner.api.urls')),

    (r'^login/$', login),

    (r'^admin/', include(admin.site.urls)),

    (r'^static_files/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': PROJECT_ROOT + "/static_files/"}),

)
