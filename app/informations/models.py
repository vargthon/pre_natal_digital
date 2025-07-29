from django.db import models

class Information(models.Model):
    """
    Model to store information about various entities.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Information'
        verbose_name_plural = 'Informations'
        ordering = ['order']
