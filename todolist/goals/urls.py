from django.urls import path

from goals.views import category, goal, comment, board

app_name = 'goals'

urlpatterns = [
    # Category views
    path('goal_category/create', category.GoalCategoryCreateView.as_view(), name='create-category'),
    path('goal_category/list', category.GoalCategoryListView.as_view(), name='category-list'),
    path('goal_category/<pk>', category.GoalCategoryView.as_view(), name='category'),
    # Goal views
    path('goal/create', goal.GoalCreateView.as_view(), name='create-goal'),
    path('goal/list', goal.GoalListView.as_view(), name='goal-list'),
    path('goal/<pk>', goal.GoalView.as_view(), name='goal'),
    # Comment views
    path('goal_comment/create', comment.GoalCommentCreateView.as_view(), name='create-comment'),
    path('goal_comment/list', comment.GoalCommentListView.as_view(), name='comment-list'),
    path('goal_comment/<pk>', comment.GoalCommentView.as_view(), name='comment'),
    # Board views
    path('board/create', board.BoardCreateView.as_view(), name='create-board'),
    path('board/list', board.BoardListView.as_view(), name='board-list'),
    path('board/<pk>', board.BoardView.as_view(), name='board'),
]
