from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from meal.models import Meal

import datetime

class Day(models.Model):

    DAYS_OF_WEEK = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                    'saturday', 'sunday']

    DAY_CHOICES = (
        (DAYS_OF_WEEK[0], 'Monday'),
        (DAYS_OF_WEEK[1], 'Tuesday'),
        (DAYS_OF_WEEK[2], 'Wednesday'),
        (DAYS_OF_WEEK[3], 'Thursday'),
        (DAYS_OF_WEEK[4], 'Friday'),
        (DAYS_OF_WEEK[5], 'Saturday'),
        (DAYS_OF_WEEK[6], 'Sunday'),
    )

    name = models.CharField(max_length = 100)
    type = models.CharField(max_length = 20, choices=DAY_CHOICES)
    date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False):
        self.name = self.date.strftime('%a %b %d, %Y')
        self.slug = slugify(self.name)
        super(Day, self).save(force_insert, force_update)

    def get_absolute_url(self):
        return ('mealweek_day_detail', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)


class Week(models.Model):
    #date must be unique
    #and when users involved, user+date combo
    #is what must be unique
    date = models.DateField()
    name = models.CharField(max_length = 100, editable=False)
    days = models.ManyToManyField(Day, editable=False)
    slug = models.SlugField(unique=True, editable=False)

    class Meta:
        pass

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False):
        """
        if date != monday:
            date = the previous monday

        name = self.date to self.date+6

        """
        #If self.date is not a Monday, then make it a Monday
        date = self.date
        weekday = date.weekday()
        if weekday != 0:
            a_monday = date - datetime.timedelta(days=weekday)
            self.date = a_monday

        start_of_week = self.date
        end_of_week = self.date + datetime.timedelta(days=6)
        self.name = "%s to %s" % (start_of_week.strftime('%a %b %d, %Y'),
                                  end_of_week.strftime('%a %b %d, %Y'),)

        self.slug = slugify(self.date.strftime('%a %b %d, %Y'))

        super(Week, self).save(force_insert, force_update)
    
    def get_absolute_url(self):
        return ('mealweek_week_detail', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)


class MealType(models.Model):
    name = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.name


class Entry(models.Model):
    meal = models.ForeignKey(Meal)
    day = models.ForeignKey(Day, editable=False)
    meal_type = models.ForeignKey(MealType)

    def __unicode__(self):
        return "%s %s" % (self.meal, self.meal_type)


def week_post_save_handler(sender, instance, **kwargs):
    #check first to make sure this week has no days
    #(I *might* have seen some duplicate behaviour)

    for counter, day in enumerate(Day.DAYS_OF_WEEK):
        d = Day(type=day)
        d.date = instance.date + datetime.timedelta(days=counter)
        d.save()
        instance.days.add(d)

models.signals.post_save.connect(week_post_save_handler, sender=Week)


def week_pre_delete_handler(sender, instance, **kwargs):
    instance.days.all().delete()

models.signals.pre_delete.connect(week_pre_delete_handler, sender=Week)