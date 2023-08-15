from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.serializers import BaseSerializer

from goals.filters import GoalFilter
from goals.models import Goal
from goals.serializers import GoalCreateSerializer, GoalSerializer


class GoalCreateView(CreateAPIView):
    """
    Create a new goal instance with the requesting user as an author
    """
    queryset: QuerySet = Goal.objects.all()
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated,)
    serializer_class: BaseSerializer = GoalCreateSerializer


class GoalListView(ListAPIView):
    """
    Return a list of all goals owned by the requesting user
    """
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )
    serializer_class: BaseSerializer = GoalSerializer

    filter_backends: tuple[BaseFilterBackend, ...] = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_class = GoalFilter
    ordering_fields: tuple[str, ...] = ('title', 'created')
    ordering: tuple[str, ...] = ('title', )
    search_fields: tuple[str, ...] = ('title', 'description')

    def get_queryset(self) -> QuerySet:
        return Goal.objects.filter(user=self.request.user)


class GoalView(RetrieveUpdateDestroyAPIView):
    """
    retrieve:
    Return the given goal

    update:
    Update all alterable fields of the given goal

    partial_update:
    Update one or more of the alterable fields of the given goal

    destroy:
    Set the given goal's status to 'archived'
    """
    serializer_class: BaseSerializer = GoalSerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )

    def get_queryset(self) -> QuerySet:
        return Goal.objects.filter(user=self.request.user)

    def perform_destroy(self, instance: Goal) -> None:
        instance.status = instance.Status.archived
        instance.save()
