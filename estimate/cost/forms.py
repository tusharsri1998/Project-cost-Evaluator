from django import forms
from .models import Work,Project, Employee
from django.contrib.auth.models import User
class newform(forms.ModelForm):
     # pid = forms.CharField(max_length=10)
     # percent=forms.IntegerField()
     class Meta:
        model = Work
        fields = ['pid', 'percent']

class newform1(forms.ModelForm):
    # p_id1 = forms.IntegerField()
    # p_name1 = forms.CharField()

    class Meta:
        model = Project
        fields = ['p_id', 'p_name']
