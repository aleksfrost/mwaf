from django.contrib import admin

# Register your models here.
from .models import Question, Users, Answer, Anchor

admin.site.register(Question)
admin.site.register(Users)
admin.site.register(Answer)
admin.site.register(Anchor)

