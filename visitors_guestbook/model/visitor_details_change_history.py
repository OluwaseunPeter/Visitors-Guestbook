from django.db import models
from django.utils import timezone

from ..models import Visitor , VisitHistory


#fields that can change over time, sometimes due to typo errors
VISITORS_NAME = "name"
VISITORS_ADDRESS = "address"

field_choice =  [
    (VISITORS_NAME , "Visitor Name") ,
    (VISITORS_ADDRESS , "Visitor Address") ,
]

class VisitorDetailChangeHistory(models.Model):
    visitor =  models.ForeignKey(Visitor , on_delete = models.CASCADE)
    history =  models.ForeignKey(VisitHistory , on_delete = models.CASCADE)

    date_created = models.DateTimeField(default =  timezone.now ,editable=False)

    field = models.CharField(max_length=100 , choices= field_choice)
    from_value = models.CharField(max_length=100)
    to_value = models.CharField(max_length=100)

    deleted =  models.BooleanField(default=False , editable=False)
    deleted_date = models.DateTimeField(null =  True , editable=False)

    def __str__(self):
        return f"{self.visitor.name} - {self.field} - Change From: {self.from_value}, Change To: {self.to_value}"