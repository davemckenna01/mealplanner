from django.conf.urls.defaults import *

from mealweek.views.lists import list_detail, list_list, list_list_top_level

urlpatterns = patterns('',


                        url(r'^$',
                            list_list_top_level,
                            name='mealweek_list_list_top_level'),

                        url(r'^(?P<model>(week|day|meal|dish))/(?P<slug>[-\w]+)/$',
                            list_detail,
                            name='mealweek_list_detail'),

                        url(r'^(?P<model>(week|day|meal|dish))/$',
                            list_list,
                            name='mealweek_list_list'),


)
