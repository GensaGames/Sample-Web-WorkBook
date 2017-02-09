from django.contrib import admin

from .models import Choice, Question, Articles


class ArticlesAdmin(admin.ModelAdmin):
    search_fields = ['articles_tittle']
    list_filter = ['pub_date']
    list_display = ('articles_tittle', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None, {'fields': ['articles_tittle']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('Main text', {'fields': ['articles_html_text'], 'classes': ['collapse']}),
    ]


## --------------------------------------------------

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['question_text']
    list_filter = ['pub_date']
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Articles, ArticlesAdmin)
