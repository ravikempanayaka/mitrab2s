from django.conf.urls import url

from . import views
from .views.question import QuestionView
from .views.question_lookup import QuestionLookUpView, UserLookupView, QuestionMaxHourView, QuestionHighestVoteView

urlpatterns = [
    url(r'^questions/$', QuestionView.as_view()),
    url(r'^question_lookup/$', QuestionLookUpView.as_view()),
    url(r'^user_lookup/$', UserLookupView.as_view()),
    url(r'^question_max_hour/$', QuestionMaxHourView.as_view()),
    url(r'^question_highest_vote/$', QuestionHighestVoteView.as_view())
]
