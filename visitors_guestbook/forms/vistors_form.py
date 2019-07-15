from django import forms
from ..models import Visitor

class VisitorsForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Visitor
        fields = ["name" , "address" ]