import logging
from django.db.models.aggregates import Max
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..utils.utils import execute_query_return_query_result
from ..models import Question, Answer
from django.contrib.auth.models import User

LOGGER = logging.getLogger(__name__)


class QuestionLookUpView(APIView):
    """

    """

    def get(self, request, **kwargs):
        """

        :param request:
        :return:
        """
        query = """select question_text
                   from question"""
        data = execute_query_return_query_result(query=query)
        print("data", data)

        user_id = self.kwargs['user_id']
        LOGGER.debug("User ID: %s", user_id)

        if 'question_key' in request.data['question_key']:
            question_asked_by_user = Question.objects.filter(user_id=user_id).distinct('question_text').values(
                'question_text')
            LOGGER.debug("Question asked by user data: %s", question_asked_by_user)
            return Response(data=question_asked_by_user, status=status.HTTP_200_OK)
        else:
            LOGGER.debug("question key not in the request")

        if 'answer_key' in request.data['answer_key']:
            answer_asked_by_user = Answer.objects.filter(user_id=user_id).distinct('answer_text').values('answer_text')
            LOGGER.debug("Answer asked by user data: %s", answer_asked_by_user)
            return Response(data=answer_asked_by_user, status=status.HTTP_200_OK)
        else:
            LOGGER.debug("question key not in the request")

        if 'upvote_key' in request.data['upvote-key']:
            upvote_by_user = Answer.objects.filter(user_id=user_id).values('upvote')
            LOGGER.debug("Upvote updated data: %s", upvote_by_user)
            return Response(data=upvote_by_user, status=status.HTTP_200_OK)
        else:
            LOGGER.debug("question key not in the request")

        if 'question_id' in request.query_params['question_id']:
            question_id = request.query_params['question_id']
            answer_qiven_question_data = Answer.objects.filter(question_id=question_id,
                                                               user_id=user_id).values('answer_text')
            LOGGER.debug("answer_qiven_question_data: %s", answer_qiven_question_data)
            return Response(data=answer_qiven_question_data, status=status.HTTP_200_OK)
        else:
            LOGGER.debug("question id not in the request")

        return Response(data=None, status=status.HTTP_400_BAD_REQUEST)


class UserLookupView(APIView):
    """

    """
    @staticmethod
    def get(self, request):
        """

        :param self:
        :param request:
        :return:
        """
        user_list = list()
        user_list_of_dict = Answer.objects.values('user_id').annotate(upvote=Max('upvote'))
        for data in user_list_of_dict:
            user_id = data['user_id']
            user_name = User.objects.get(id=user_id).username
            post_set = {
                'user_id': user_id,
                'user_name': user_name
            }
            user_list.append(post_set)

        return Response(data=user_list, status=status.HTTP_200_OK)
