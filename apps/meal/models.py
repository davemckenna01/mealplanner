from django.db import models
from django.template.defaultfilters import slugify

from markdown import markdown

class CustomIngredient(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return ('meal_custom_ingredient_detail', (), { 'object_id': self.id })
    get_absolute_url = models.permalink(get_absolute_url)


class Dish(models.Model):
    name = models.CharField(max_length=100, unique=True)
    custom_ingredients = models.ManyToManyField(CustomIngredient, blank=True, through='DishCustomIngredient')
    notes = models.TextField(max_length=10000, blank=True)
    notes_html = models.TextField(max_length=10000, blank=True, editable=False)
    slug = models.SlugField(unique=True, editable=False)

    class Meta:
        verbose_name_plural = 'Dishes'

    def save(self, force_insert=False, force_update=False):
        self.notes_html = markdown(self.notes)
        self.slug = slugify(self.name)
        super(Dish, self).save(force_insert, force_update)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return ('meal_dish_detail', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)


class DishCustomIngredient(models.Model):
    dish = models.ForeignKey(Dish)
    custom_ingredient = models.ForeignKey(CustomIngredient)
    measurement = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return "%s_%s" % (self.dish, self.custom_ingredient)


class Meal(models.Model):
    name = models.CharField(max_length=100, unique=True)
    dishes = models.ManyToManyField(Dish, blank=True)
    slug = models.SlugField(unique=True, editable=False)

    class Meta:
        pass

    def save(self, force_insert=False, force_update=False):
        self.slug = slugify(self.name)
        super(Meal, self).save(force_insert, force_update)

    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return ('meal_meal_detail', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)