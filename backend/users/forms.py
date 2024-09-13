import datetime

from django import  forms
from django.contrib.auth import get_user_model



class UserForm(forms.ModelForm):
    this_year = datetime.date.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100,this_year-5))))

    photo = forms.ImageField
    class Meta:
        model = get_user_model()
        fields = ["photo", "date_birth",]