from django.conf.urls import url

from . import views
from .views.question import QuestionView
from .views.question_lookup import QuestionLookUpView

urlpatterns = [
    url(r'^questions/$', QuestionView.as_view()),
    url(r'^question_lookup/$', QuestionLookUpView.as_view())
]
