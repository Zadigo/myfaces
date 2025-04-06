from django.urls import re_path
from scores.api import views

app_name = 'scores_api'

urlpatterns = [
    re_path(
        r'^session/(?P<session>sess\_[a-zA-Z0-9]+\-[a-zA-Z0-9]+)$',
        views.SessionValidity.as_view(),
        name='session_validity'
    ),
    # re_path(
    #     r'^user-details',
    #     views.user_details_view
    # ),
    re_path(
        r'^ranking',
        views.ranking_view
    ),
    re_path(
        r'^scores/submit$',
        views.SubmitScores.as_view(),
        name='submit_scores'
    ),
    re_path(
        r'^session$',
        views.CreateNewSession.as_view(),
        name='new_session'
    ),
    re_path(
        r'^session-key$',
        views.NewSessionKey.as_view(),
        name='session_key'
    ),
    re_path(
        r'^emotions$',
        views.ListEmotions.as_view(),
        name='list_emotions'
    ),
    re_path(
        r'^random$',
        views.ListRandomFaces.as_view(),
        name='list_random_faces'
    ),
    re_path(
        r'^$',
        views.ListAllFaces.as_view(),
        name='list_all_faces'
    )
]
