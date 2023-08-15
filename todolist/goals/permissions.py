from rest_framework import permissions
from rest_framework.request import Request

from goals.models import BoardParticipant, Board, GoalCategory


class BoardPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, view, obj: Board) -> bool:
        _filters: dict = {'user_id': request.user.id, 'board_id': obj.id}
        if request.method not in permissions.SAFE_METHODS:
            _filters['role'] = BoardParticipant.Role.owner

        return BoardParticipant.objects.filter(**_filters).exists()


class CategoryPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, view, obj: GoalCategory) -> bool:
        _filters: dict = {'user_id': request.user.id, 'board_id': obj.board_id}
        if request.method not in permissions.SAFE_METHODS:
            _filters['role__in'] = (BoardParticipant.Role.owner, BoardParticipant.Role.writer)

        return BoardParticipant.objects.filter(**_filters).exists()
