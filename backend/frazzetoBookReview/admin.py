from django.contrib import admin
from frazzetoBookReview.models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_instructor']
    list_filter = ['is_instructor']
    search_fields = ['user__email']
