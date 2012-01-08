from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_detail
from django.views.generic.create_update import delete_object

from mealweek.forms import EntryForm
from mealweek.models import Day, Entry

def day_detail(request, slug):

    day = Day.objects.get(slug=slug)
    entries = Entry.objects.filter(day=day)

    if request.method == 'POST':
        form = EntryForm(data=request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.day = day
            entry.save()
            return HttpResponseRedirect(reverse('mealweek_day_detail',
                                            kwargs={'slug': slug }))
    else:
        form = EntryForm()

    return object_detail(request, slug=slug,
                                  queryset=Day.objects.all(),
                                  template_name='mealweek/day_detail.html',
                                  extra_context={'form':form,
                                                 'entries': entries,
                                                },
                        )

def day_detail_delete_entry(request, day_slug, entry_id):
    pdr = reverse('mealweek_day_detail', kwargs={'slug': day_slug })
    return delete_object(request, model=Entry,
                    object_id=entry_id,
                    post_delete_redirect=pdr,
                    )