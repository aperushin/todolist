from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import BaseFilterBackend, OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.serializers import BaseSerializer

from goals.models import GoalComment
from goals.permissions import CommentPermission
from goals.serializers import GoalCommentCreateSerializer, GoalCommentSerializer


class GoalCommentCreateView(CreateAPIView):
    """
    Create a new comment instance with the requesting user as an author
    """
    queryset: QuerySet = GoalComment.objects.all()
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )
    serializer_class: BaseSerializer = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    """
    Return a list of all comments owned by the requesting user
    """
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )
    serializer_class: BaseSerializer = GoalCommentSerializer

    filter_backends: tuple[BaseFilterBackend, ...] = (OrderingFilter, DjangoFilterBackend)
    ordering: tuple[str, ...] = ('-created', )
    ordering_fields: tuple[str, ...] = ('created', 'updated')
    filterset_fields: tuple[str, ...] = ('goal', )

    def get_queryset(self) -> QuerySet:
        return GoalComment.objects.filter(goal__category__board__participants__user_id=self.request.user.id)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    """
    retrieve:
    Return the given comment

    update:
    Update all alterable fields of the given goal

    partial_update:
    Update one or more of the alterable fields of the given goal

    destroy:
    Delete the given comment instance
    """
    serializer_class: BaseSerializer = GoalCommentSerializer
    permission_classes: tuple[BasePermission, ...] = (CommentPermission, )

    def get_queryset(self) -> QuerySet:
        return GoalComment.objects.filter(goal__category__board__participants__user_id=self.request.user.id)
