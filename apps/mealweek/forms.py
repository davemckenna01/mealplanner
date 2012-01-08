from django import forms

from django.core.exceptions import ObjectDoesNotExist

import datetime

from mealweek.models import Week, Day, Entry

        
class WeekForm(forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today)
    
    class Meta:
        model = Week

    def clean_date(self):

        #If date is not a Monday, then make it a Monday.
        #Week.date is only ever stored as a Monday, so wee need
        #to do this conversion and check here.
        date = self.cleaned_data['date']
        weekday = date.weekday()
        if weekday != 0:
            date = date - datetime.timedelta(days=weekday)

        try:
            Week.objects.get(date=date)
        except ObjectDoesNotExist:
            pass
        else:
            raise forms.ValidationError("You have already created a schdule for that week...")

        #check to make sure it's not in the past behind the current week
        #b/c why would you want to plan for the past????? DOYEEE

        today = datetime.date.today()
        print today
        today_weekday = today.weekday()
        print today_weekday
        if today_weekday != 0:
            current_weeks_monday = today - datetime.timedelta(days=today_weekday)
        else:
            current_weeks_monday = today
        
        print current_weeks_monday

        if date < current_weeks_monday:
            raise forms.ValidationError("You're living in the past, man.")

        return self.cleaned_data['date']


class DayForm(forms.ModelForm):

    class Meta:
        model = Day

class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry