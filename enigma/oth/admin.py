from django.contrib import admin

from .models import Question, Image, Phase

class ImageAdmin(admin.ModelAdmin):
    #list_display= ('image_img',)
    readonly_fields = ('image_img',)

admin.site.register(Question)
admin.site.register(Image, ImageAdmin)
admin.site.register(Phase)
