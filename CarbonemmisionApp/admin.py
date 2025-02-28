from django.contrib import admin
from .models import Equipment, Event, BlogPost, Organization, CarbonEmission

# Register your models here.

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    search_fields = ('title', 'description', 'location')
    list_filter = ('date',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry_type', 'created_at')
    search_fields = ('name', 'industry_type')
    list_filter = ('industry_type',)

@admin.register(CarbonEmission)
class CarbonEmissionAdmin(admin.ModelAdmin):
    list_display = ('organization', 'date', 'total_emissions', 'predicted_emissions')
    list_filter = ('organization', 'date')
    search_fields = ('organization__name',)
    date_hierarchy = 'date'
