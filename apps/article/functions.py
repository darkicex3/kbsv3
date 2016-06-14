
# FUNCTION FOR MODELS IN ADMIN INTERFACE


def make_published(modeladmin, request, queryset):
    for o in queryset:
        o.status = 'p'
        o.save()
make_published.short_description = "Mark selected as published"


def make_draft(modeladmin, request, queryset):
    for o in queryset:
        o.status = 'd'
        o.save()
make_draft.short_description = "Mark selected as draft"


def make_withdrawn(modeladmin, request, queryset):
    for o in queryset:
        o.status = 'w'
        o.save()
make_withdrawn.short_description = "Mark selected as withdrawn"


def duplicate_event(modeladmin, request, queryset):
    for o in queryset:
        o.id = None
        o.save()
duplicate_event.short_description = "Duplicate selected record"


def deleteall(modeladmin, request, queryset):
    for a in queryset:
        a.delete()
deleteall.short_description = "Delete all selected > 999 record"


def make_activated(modeladmin, request, queryset):
    for o in queryset:
        o.activated = True
        o.save()
make_activated.short_description = "Mark selected as activated"


def make_desactivated(modeladmin, request, queryset):
    for o in queryset:
        o.activated = False
        o.save()
make_desactivated.short_description = "Mark selected as desactivated"


def reset_counter(modeladmin, request, queryset):
    for o in queryset:
        o.useful_counter = 0
        o.favorite_counter = 0
        o.view_counter = 0
        o.save()
make_published.short_description = "Mark selected as published"