from django.db import models
from django.contrib.auth.models import User

PROG=(
    ('Done','Done'),
    ('In progress','In progress'),
    ('Not started','Not started'),
)
class task(models.Model):
    Attribute=models.CharField(max_length=100,null=True)
    Task=models.CharField(max_length=100,null=True)
    Duration=models.PositiveIntegerField(null=True)
    Predecessors=models.CharField(max_length=100,null=True)
    EarliestST=models.PositiveIntegerField(null=True)
    LatestST=models.PositiveIntegerField(null=True)
    tfloat=models.PositiveIntegerField(null=True)
    ffloat=models.PositiveIntegerField(null=True)
    RequiredRT=models.CharField(max_length=100,null=True)
    EstimatedEf=models.PositiveIntegerField(null=True)
    Staffid=models.PositiveIntegerField(null=True)
    Progress=models.CharField(max_length=50,choices=PROG,default='Not Started')
    def __str__(self):
        return f'{self.Task}'
    
    def get_predecessors_list(self):
        if self.Predecessors:
            return self.Predecessors.split(',')
        return []
    
    
