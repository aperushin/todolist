from django.db import transaction
from django.db.models import QuerySet
from rest_framework.filters import BaseFilterBackend, OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.serializers import BaseSerializer

from goals.models import Board, Goal, BoardParticipant
from goals.permissions import BoardPermission
from goals.serializers import BoardCreateSerializer, BoardSerializer


class BoardCreateView(CreateAPIView):
    """
    Create a new board instance and a new board participant instance for it with the requesting user as the owner
    """
    queryset: QuerySet = Board.objects.all()
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated,)
    serializer_class: BaseSerializer = BoardCreateSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        BoardParticipant.objects.create(user=self.request.user, board=serializer.save())


class BoardListView(ListAPIView):
    """
    Return a list of all active boards with the requesting user as the board's participant
    """
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated,)
    serializer_class: BaseSerializer = BoardCreateSerializer
    filter_backends: tuple[BaseFilterBackend, ...] = (OrderingFilter, )
    ordering: tuple[str, ...] = ('title', )

    def get_queryset(self) -> QuerySet:
        return Board.objects.filter(participants__user_id=self.request.user.id, is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView):
    """
    retrieve:
    Return the given board

    update:
    Update title and participants of the given board

    partial_update:
    Update title or participants of the given board

    destroy:
    Set the given board's is_deleted flag to True, update all child objects accordingly
    """
    serializer_class: BaseSerializer = BoardSerializer
    permission_classes: tuple[BasePermission, ...] = (BoardPermission, )

    def get_queryset(self) -> QuerySet:
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board) -> None:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()

            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)
