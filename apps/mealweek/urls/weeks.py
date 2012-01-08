from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object


from mealweek.models import Week
from mealweek.forms import WeekForm

urlpatterns = patterns('',


                        url(r'^$',
                            object_list,
                            { 'queryset': Week.objects.all(),
                               'paginate_by': 20 },
                            name='mealweek_week_list'),

                        url(r'^create/$',
                            create_object,
                            { 'form_class': WeekForm,
                              'extra_context': {'operation': 'create'},
                            },
                            name='mealweek_week_create'),

                        url(r'^(?P<slug>[-\w]+)/$',
                            object_detail,
                            { 'queryset': Week.objects.all()},
                            name='mealweek_week_detail'),

                        url(r'^delete/(?P<slug>[-\w]+)/$',
                            delete_object,
                            { 'model': Week,
                              'post_delete_redirect': '/schedule/weeks/',
                            },
                            name='mealweek_week_delete'),


)
