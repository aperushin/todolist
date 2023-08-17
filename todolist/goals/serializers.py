from django.db import transaction
from django.db.models import QuerySet
from rest_framework import serializers

from core.models import User
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from core.serializers import ProfileSerializer


class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        read_only_fields = ('id', 'created', 'updated', 'is_deleted')
        fields = '__all__'


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.editable_choices)
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'board')


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'is_deleted')

    def update(self, instance: Board, validated_data: dict) -> Board:
        owner: User = validated_data.pop('user')
        new_participants: list[dict] = validated_data.pop('participants')
        new_by_id: dict[int, dict] = {pa['user'].id: pa for pa in new_participants}

        # Exclude the owner from the query since the board's owner should not be deleted
        existing_participants: QuerySet = instance.participants.exclude(user=owner)
        existing_by_id: dict[int, BoardParticipant] = {pa.user_id: pa for pa in existing_participants}

        with transaction.atomic():
            # Delete existing participants that are not in the new_participants
            for uid, existing_participant in existing_by_id.items():
                if uid not in new_by_id.keys():
                    existing_participant.delete()

            # Add new participants, change roles for the existing ones
            for uid, participant_data in new_by_id.items():
                role = participant_data['role']

                if uid in existing_by_id.keys() and existing_by_id[uid].role != role:
                    existing_by_id[uid].role = role
                    existing_by_id[uid].save()
                else:
                    BoardParticipant.objects.create(
                        user=participant_data['user'],
                        board=instance,
                        role=role,
                    )

        if title := validated_data.get('title'):
            instance.title = title
            instance.save()
        return instance


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'board', 'is_deleted')


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate(self, attrs: dict) -> dict:
        if not BoardParticipant.objects.filter(
            user_id=attrs['user'].id,
            board_id=attrs['board'].id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists():
            raise serializers.ValidationError('No permission to create categories on this board')

        return attrs


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_category(self, category: GoalCategory) -> GoalCategory:
        if category.is_deleted:
            raise serializers.ValidationError('Cannot use a deleted category')

        if category.user != self.context['request'].user:
            raise serializers.ValidationError('Not an owner of this category')

        return category


class GoalCreateSerializer(GoalSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class GoalCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')


class GoalCommentCreateSerializer(GoalCommentSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, attrs: dict) -> dict:
        if not BoardParticipant.objects.filter(
            user_id=attrs['user'].id,
            board_id=attrs['goal'].category.board_id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists():
            raise serializers.ValidationError('No permission to create comments on this board')

        return attrs
