from django.db import models

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Status(models.Model):
    title = models.CharField(max_length=120) 
    def __str__(self):
        return self.title
    
class Step(models.Model):
    todo = models.ForeignKey(Todo,on_delete=models.CASCADE,related_name="steps")
    name = models.CharField(max_length=120)
    days = models.IntegerField()
    status = models.ForeignKey(Status,on_delete=models.CASCADE,related_name="status",null=True)
    def __str__(self):
        return self.name