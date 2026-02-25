from django.contrib import admin

from .models import Group, IPRange, Note, Relation


class GroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(Group, GroupAdmin)


class IPRangeAdmin(admin.ModelAdmin):
    pass


admin.site.register(IPRange, IPRangeAdmin)


class RelationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Relation, RelationAdmin)


class NoteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Note, NoteAdmin)
