from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=100, blank=True, null=True)


    def __str__(self) -> str:
        return self.name
