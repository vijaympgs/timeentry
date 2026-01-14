from django.contrib import admin
from .models import Company, OrganizationalUnit, Position, RatingScale, Course

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    search_fields = ['name', 'code']

@admin.register(OrganizationalUnit)
class OrganizationalUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'unit_type']
    search_fields = ['name', 'code']

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'position_code']
    search_fields = ['title', 'position_code']

@admin.register(RatingScale)
class RatingScaleAdmin(admin.ModelAdmin):
    list_display = ['scale_name', 'scale_code']
    search_fields = ['scale_name', 'scale_code']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'course_code']
    search_fields = ['course_name', 'course_code']

print("Admin test file loaded successfully")
