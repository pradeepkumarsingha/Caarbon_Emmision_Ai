from django.db import models
from django.utils import timezone

# Create your models here.

class Equipment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='equipment/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Organization(models.Model):
    name = models.CharField(max_length=200)
    industry_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class CarbonEmission(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateField()
    energy_consumption = models.FloatField()  # in kWh
    transportation_emissions = models.FloatField()  # in kg CO2
    waste_emissions = models.FloatField()  # in kg CO2
    total_emissions = models.FloatField()  # in kg CO2
    predicted_emissions = models.FloatField(null=True, blank=True)  # AI prediction

    def __str__(self):
        return f"{self.organization.name} - {self.date}"

    class Meta:
        ordering = ['date']
