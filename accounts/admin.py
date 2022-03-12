from django.contrib import admin
from accounts.models import Account, AuthToken


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "mobile_number",
	    "email",
    )
    list_display_links = (
        "id",
        "mobile_number",
	    "email",
    )

    search_fields = ("mobile_number", "email")


class AuthTokenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "key",
    )
    list_display_links = (
        "id",
        "user",
        "key",
    )
    raw_id_fields = ("user",)
    search_fields = ("user",)


admin.site.register(AuthToken, AuthTokenAdmin)
admin.site.register(Account, AccountAdmin)
