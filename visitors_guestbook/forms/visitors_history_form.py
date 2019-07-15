from django import forms
from ..models import VisitHistory

class VisitHistoryForm(forms.ModelForm):
    class Meta:
        model = VisitHistory
        fields = ["to_see" , "visit_purpose" , "comment" ]