from django.contrib import admin

from myapp.models import User, Cart


# Register your models here.
@admin.register(User)

class UserAdmin(admin.ModelAdmin):
    list_display= ['first_name','last_name','Email','password','mobile_number']

admin.site.register(Cart)