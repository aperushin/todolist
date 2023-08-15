from typing import OrderedDict

import pytest
from django.utils import timezone
from pytest_factoryboy import register

from tests.factories import UserFactory, GoalCategoryFactory, BoardFactory, BoardParticipantFactory, GoalFactory

register(UserFactory)
register(GoalCategoryFactory)
register(GoalFactory)
register(BoardFactory)
register(BoardParticipantFactory)


class Helpers:
    @staticmethod
    def trim_dates(response_data: OrderedDict) -> None:
        """
        Trim dates from responses to fit the format %Y-%m-%dT%H:%M

        This is needed to prevent tests failing because of differences in seconds/millisecond
        between the creation of objects and the timestamps in expected data
        """
        response_data['created'] = response_data['created'][:-11]
        response_data['updated'] = response_data['updated'][:-11]
        if participants := response_data.get('participants'):
            for i, _ in enumerate(participants):
                response_data['participants'][i]['created'] = response_data['participants'][i]['created'][:-11]
                response_data['participants'][i]['updated'] = response_data['participants'][i]['updated'][:-11]


@pytest.fixture
def helpers():
    return Helpers


@pytest.fixture
def formatted_now() -> str:
    """
    Return datetime string in format %Y-%m-%dT%H:%M
    """
    return timezone.now().strftime('%Y-%m-%dT%H:%M')
