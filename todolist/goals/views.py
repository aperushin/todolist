from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.db.models import QuerySet
from rest_framework.serializers import BaseSerializer
from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend
from django_filters.rest_framework import DjangoFilterBackend

from goals.models import GoalCategory, Goal, Status, GoalComment
from goals.serializers import (
    GoalCategoryCreateSerializer,
    GoalCategorySerializer,
    GoalCreateSerializer,
    GoalSerializer,
    GoalCommentCreateSerializer,
    GoalCommentSerializer,
)
from goals.filters import GoalFilter


class GoalCategoryCreateView(CreateAPIView):
    queryset: QuerySet = GoalCategory.objects.all()
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )
    serializer_class: BaseSerializer = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )
    serializer_class: BaseSerializer = GoalCategorySerializer

    filter_backends: tuple[BaseFilterBackend, ...] = (OrderingFilter, SearchFilter)
    ordering_fields: tuple[str, ...] = ('title', 'created')
    ordering: tuple[str, ...] = ('title', )
    search_fields: tuple[str, ...] = ('title', )

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    serializer_class: BaseSerializer = GoalCategorySerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory):
        instance.is_deleted = True
        instance.save()


class GoalCreateView(CreateAPIView):
    queryset: QuerySet = Goal.objects.all()
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated,)
    serializer_class: BaseSerializer = GoalCreateSerializer


class GoalListView(ListAPIView):
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )
    serializer_class: BaseSerializer = GoalSerializer

    filter_backends: tuple[BaseFilterBackend, ...] = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_class = GoalFilter
    ordering_fields: tuple[str, ...] = ('title', 'created')
    ordering: tuple[str, ...] = ('title', )
    search_fields: tuple[str, ...] = ('title', 'description')

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class GoalView(RetrieveUpdateDestroyAPIView):
    serializer_class: BaseSerializer = GoalSerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_destroy(self, instance: Goal):
        instance.status = Status.archived
        instance.save()


class GoalCommentCreateView(CreateAPIView):
    queryset: QuerySet = GoalComment.objects.all()
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )
    serializer_class: BaseSerializer = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )
    serializer_class: BaseSerializer = GoalCommentSerializer

    filter_backends: tuple[BaseFilterBackend, ...] = (OrderingFilter, DjangoFilterBackend)
    ordering: tuple[str, ...] = ('-created', )
    ordering_fields: tuple[str, ...] = ('created', 'updated')
    filterset_fields: tuple[str, ...] = ('goal', )

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    serializer_class: BaseSerializer = GoalCommentSerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)
