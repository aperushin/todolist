from rest_framework import serializers

from goals.models import GoalCategory, Goal, GoalComment
from core.serializers import ProfileSerializer


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'is_deleted')


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_category(self, category):
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

    def validate_goal(self, goal):
        if goal.user != self.context['request'].user:
            raise serializers.ValidationError('Not an owner of this goal')

        return goal


class GoalCommentCreateSerializer(GoalCommentSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
