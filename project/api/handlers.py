from piston.handler import BaseHandler
from piston.utils import rc

from meal.models import Dish, Meal, CustomIngredient
from mealweek.models import Week, Day, Entry

from mealweek.views.lists import list_detail, list_list, list_list_top_level

class WeekHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Week
    fields = (   'name',
                 'id',
                ('days',
                    ('id','name',),
                ),
            )

    def read(self, request, id=None):

        base = Week.objects

        if id:
            return base.get(pk=id)
        else:
            return base.all() 
        

class DayHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Day
    fields = (   'name',
                 'id',
                ('entry_set',
                    ('id',
                    ('meal',
                        ('id','name',),
                    ),
                    ('meal_type',
                        ('id','name',),
                    ),
                ),
                ),
            )

    def read(self, request, id=None):

        base = Day.objects

        if id:
            #import pdb; pdb.set_trace()
            return base.get(pk=id)
        else:
            return base.all()

    @classmethod
    def entries_custom(self, foo):
        #for some reason the fields on EntryHandler do not return
        #the fields I need... there'a s problem following the relations.
        #So I have to do this class method
        entries = foo.entry_set.all()
        entry_list = []
        for entry in entries:
            entry_item = {}

            day_item = {}
            day_item['id'] = entry.day.id
            day_item['name'] = entry.day.name
            entry_item['day'] = day_item

            meal_type_item={}
            meal_type_item['id'] = entry.meal_type.id
            meal_type_item['name'] = entry.meal_type.name
            entry_item['meal_type'] = meal_type_item

            meal_item={}
            meal_item['id'] = entry.meal.id
            meal_item['name'] = entry.meal.name

            dish_list = []
            for dish in entry.meal.dishes.all():

                dish_item = {}
                dish_item['id'] = dish.id
                dish_item['name'] = dish.name

                dish_list.append(dish_item)


            meal_item['dishes'] = dish_list
            entry_item['meal'] = meal_item

            entry_list.append(entry_item)

        return entry_list


class EntryHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Entry
    fields = ('id',
                ('meal_type',
                    ('id','name',),
                ),
                ('meal',
                    ('id','name',),
                ),
                ('day',
                    ('name',),
                ),
            )

    def read(self, request, id=None):
        base = Entry.objects

        if id:
            return base.get(pk=id)
        else:
            return base.all()


class MealHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Meal
    #fields = ('name', ('dishes',('id'),), 'id')
    fields = (   'name',
                 'id',
                ('dishes',
                    ('id','name',),
                ),
            )

    def read(self, request, id=None):
        base = Meal.objects

        if id:
            return base.get(pk=id)
        else:
            return base.all()


class DishHandler(BaseHandler):
    allowed_methods = ('GET', 'DELETE', 'POST')
    model = Dish
    fields = (   'name',
                 'id',
                ('ingredients',
                    ('id','shrt_desc',),
                ),
                ('custom_ingredients',
                    ('id','name',),
                ),
            )

    def read(self, request, id=None):
        base = Dish.objects

        if id:
            return base.get(pk=id)
        else:
            return base.all()

    def delete(self, request, id=None):
        base = Dish.objects
        
        if id:
            dish = base.get(pk=id)
            dish.delete()
            return rc.DELETED
        else:
            return rc.BAD_REQUEST


    def create(self, request):


        print request.POST.get("name")
        print request.POST.get("ingredients")
        print request.POST
        #dish = Dish.create()


        return rc.CREATED


class CustomIngredientHandler(BaseHandler):
    model = CustomIngredient
    #exclude = ('id', )


class ListHandler(BaseHandler):

    def read(self, request, model=None, slug=None):

        if not model and not slug:
            return list_list_top_level(request, True)

        elif model and not slug:
            return list_list(request, model, True)

        elif model and slug:
            return list_detail(request, model, slug, True)

        else:
            pass