from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user__username')
    readonly_fields = ('created', 'updated')


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user__username', 'description')
    readonly_fields = ('created', 'updated')


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'created', 'updated')
    search_fields = ('text', 'user__username')
    readonly_fields = ('created', 'updated')


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')
    search_fields = ('title', )
    readonly_fields = ('created', 'updated')


class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'board', 'role', 'created', 'updated')
    search_fields = ('user__username', )
    readonly_fields = ('created', 'updated')


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardParticipant, BoardParticipantAdmin)
