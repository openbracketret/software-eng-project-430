from django.contrib import admin

# Register your models here.

from script.models import ScriptRedeems, Script, Customer

admin.site.register(Script)
admin.site.register(ScriptRedeems)
admin.site.register(Customer)