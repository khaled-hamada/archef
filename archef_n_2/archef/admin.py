from django.contrib import admin


from  . import models


admin.site.register(models.Part)
admin.site.register(models.ArchefUser)
admin.site.register(models.Decision)
admin.site.register(models.DecisionRecord)
admin.site.register(models.Shab)