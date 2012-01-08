from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object


from mealweek.models import Day
#from mealweek.forms import DayForm
from mealweek.views.days import day_detail, day_detail_delete_entry

urlpatterns = patterns('',


                        url(r'^(?P<slug>[-\w]+)/$',
                            day_detail,
                            name='mealweek_day_detail'),

                        #TODO: In this pattern, "day_slug" MUST be checked to belong
                        #to the proper user ... since it's just being used to
                        #redirect to the right day after the delete. Probably it
                        #will be fine as long as view day_deatil checks for
                        #proper user.
                        url(r'^(?P<day_slug>[-\w]+)/remove_meal/(?P<entry_id>\d+)/$',
                            day_detail_delete_entry,
                            name='mealweek_day_detail_delete_entry'),

)
