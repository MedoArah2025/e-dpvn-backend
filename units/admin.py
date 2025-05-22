from django.contrib import admin
from .models import Unite, ActivityGroup, UniteActivityGroup

#
# Inline pour gérer les affectations sur la page Unite
#
class UniteActivityGroupInlineOnUnite(admin.TabularInline):
    model = UniteActivityGroup
    extra = 1
    verbose_name = "Groupe d’activité"
    verbose_name_plural = "Groupes d’activité"

@admin.register(Unite)
class UniteAdmin(admin.ModelAdmin):
    list_display  = ("nom", "type", "parent", "created_at", "get_groups")
    list_filter   = ("type",)
    search_fields = ("nom",)
    inlines       = [UniteActivityGroupInlineOnUnite]

    def get_groups(self, obj):
        return ", ".join(uag.group.nom for uag in obj.affectations.all())
    get_groups.short_description = "Groupes d’activités"

#
# Inline pour gérer les affectations sur la page ActivityGroup
#
class UniteActivityGroupInlineOnGroup(admin.TabularInline):
    model   = UniteActivityGroup
    fk_name = "group"
    extra   = 1
    verbose_name = "Unité"
    verbose_name_plural = "Unités"

@admin.register(ActivityGroup)
class ActivityGroupAdmin(admin.ModelAdmin):
    list_display  = ("nom", "categorie", "created_at", "get_unites")
    list_filter   = ("categorie",)
    search_fields = ("nom",)
    inlines       = [UniteActivityGroupInlineOnGroup]

    def get_unites(self, obj):
        return ", ".join(uag.unite.nom for uag in obj.affectations.all())
    get_unites.short_description = "Unités"

@admin.register(UniteActivityGroup)
class UniteActivityGroupAdmin(admin.ModelAdmin):
    list_display = ("unite", "group")
    list_filter  = ("group",)
