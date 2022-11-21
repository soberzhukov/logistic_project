from django.contrib import admin

from users.models import User, ConfirmPassword, ConfirmPhone


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'patronymic', 'email', 'push_token', 'is_blocked',
                    'cause_blocked', 'is_admin']

    def save_model(self, request, obj, form, change):

        if change:
            old_user = User.objects.get(pk=obj.pk)
            if old_user.password != obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)

        obj.save()


@admin.register(ConfirmPhone)
class ConfirmPhoneAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(ConfirmPassword)
class ConfirmPasswordAdmin(admin.ModelAdmin):
    exclude = []
