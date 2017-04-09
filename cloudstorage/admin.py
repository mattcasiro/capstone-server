from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from cloudstorage.models import Folder, File


class FileInLine(admin.TabularInline):
    model = File
    extra = 1


class FolderAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'owner',
        'created',
    )

    list_display_links = (
        'indented_title',
    )

    inlines = (FileInLine,)


class FileAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'owner',
        'folder',
        'mime_type',
        'created',
    )

admin.site.register(Folder, FolderAdmin)
admin.site.register(File, FileAdmin)
