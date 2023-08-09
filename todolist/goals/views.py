from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.db.models import QuerySet
from rest_framework.serializers import BaseSerializer
from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend
from django_filters.rest_framework import DjangoFilterBackend

from goals.models import GoalCategory, Goal, Status
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer
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
        return instance


class GoalCreateView(CreateAPIView):
    queryset: QuerySet = Goal.objects.all()
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated,)
    serializer_class: BaseSerializer = GoalCreateSerializer


class GoalListView(ListAPIView):
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )
    serializer_class: BaseSerializer = GoalSerializer

    filter_backends: tuple[BaseFilterBackend, ...] = (OrderingFilter, DjangoFilterBackend)
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
        return instance
