from django.db import transaction
from django.db.models import QuerySet
from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.serializers import BaseSerializer

from goals.models import GoalCategory, Goal
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    """
    Create a new goal category instance with the requesting user is an author
    """
    queryset: QuerySet = GoalCategory.objects.all()
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )
    serializer_class: BaseSerializer = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """
    Return a list of all active goal categories owned by the requesting user
    """
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )
    serializer_class: BaseSerializer = GoalCategorySerializer

    filter_backends: tuple[BaseFilterBackend, ...] = (OrderingFilter, SearchFilter)
    ordering_fields: tuple[str, ...] = ('title', 'created')
    ordering: tuple[str, ...] = ('title', )
    search_fields: tuple[str, ...] = ('title', )

    def get_queryset(self) -> QuerySet:
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """
    retrieve:
    Return the given category

    update:
    Update the 'title' field of the given category

    partial_update:
    Update the 'title' field of the given category

    destroy:
    Set the given category's is_deleted flag to True, set the child goals' statuses to 'archived'
    """
    serializer_class: BaseSerializer = GoalCategorySerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )

    def get_queryset(self) -> QuerySet:
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory) -> None:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.goals.update(status=Goal.Status.archived)
