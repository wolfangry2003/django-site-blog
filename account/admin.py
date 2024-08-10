from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User



UserAdmin.fieldsets[2][1]['fields'] = (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_author",
                    "special_user",
                    "groups",
                    "user_permissions",
                )

# UserAdmin.fieldsets += (
#     ("فیلد خاص من", {'fields': ("is_author", "is_superuser")})
# )

UserAdmin.list_display += ('is_author', 'is_superuser', 'is_special_user')

admin.site.register(User, UserAdmin)
# Register your models here.
