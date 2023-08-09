from django_filters import IsoDateTimeFilter
from django.db import models
from django_filters.rest_framework import FilterSet

from goals.models import Goal


class GoalFilter(FilterSet):
    """
    Filterset class for Goal list view
    """
    class Meta:
        model = Goal
        fields = {
            'due_date': ('gte', 'lte'),
            'category': ('exact', 'in'),
            'status': ('exact', 'in'),
            'priority': ('exact', 'in'),
        }

    filter_overrides = {
        models.DateTimeField: {'filter_class': IsoDateTimeFilter},
    }
