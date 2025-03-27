from django.db import models

# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=255)
    reference_point = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    
class EmergencyContact(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    relationship = models.CharField(max_length=255)
    
class PregnantWoman(models.Model):
    full_name = models.CharField(max_length=255)
    sus_card_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()
    nis_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    prefered_name = models.CharField(max_length=255, blank=True, null=True)
    race = models.CharField(max_length=50)
    ethnicity = models.CharField(max_length=50)
    work_outside_home = models.BooleanField(default=False)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    mobile_phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, blank=True, null=True)
    due_date = models.DateField()
    emergency_contact = models.ForeignKey(EmergencyContact, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.full_name