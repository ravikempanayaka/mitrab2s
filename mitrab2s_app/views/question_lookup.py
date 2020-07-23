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
        # user id get by kwrgs or get query pamars
        # user_id = self.kwargs['user_id']
        # LOGGER.debug("User ID: %s", user_id)
        # if user_id:
        #     LOGGER.debug("User id from kwargs")
        # else:
        user_id = request.query_params['user_id']

        # 1. What are the questions asked by me?
        if 'question_key' in request.query_params:
            question_asked_by_user = Question.objects.filter(user_id=user_id).distinct('question_text').values(
                'question_text')
            LOGGER.debug("Question asked by user data: %s", question_asked_by_user)
            return Response(data=question_asked_by_user, status=status.HTTP_200_OK)
        else:
            LOGGER.debug("question key not in the request")

        # 2. What are the answers given by me?
        if 'answer_key' in request.query_params:
            answer_asked_by_user = Answer.objects.filter(user_id=user_id).distinct('answer_text').values('answer_text')
            LOGGER.debug("Answer asked by user data: %s", answer_asked_by_user)
            return Response(data=answer_asked_by_user, status=status.HTTP_200_OK)
        else:
            LOGGER.debug("question key not in the request")

        # 3. What are the upvotes done by me?
        if 'upvote_key' in request.query_params:
            upvote_by_user = Answer.objects.filter(user_id=user_id).values('upvote')
            LOGGER.debug("Upvote updated data: %s", upvote_by_user)
            return Response(data=upvote_by_user, status=status.HTTP_200_OK)
        else:
            LOGGER.debug("question key not in the request")

        # 4. What are the answers to a given question?
        if 'question_id' in request.query_params:
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
    def get(self):
        """

        :param self:
        :param request:
        :return:
        """
        # 5. Who has all upvoted a given question’s answer?
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


class QuestionMaxHourView(APIView):
    """

    """

    @staticmethod
    def get(self):
        """
        6. Across the entire application, which question has had the highest number of upvotes over the past hour.
        """

        LOGGER.debug("get highest number upvote in one hour")
        query = """select max(a.upvote) as upvote,
                          q.question_text 
                    from question q 
                    join answer a on (q.id=a.question_id_id) 
                    where a.modify_datetime >= (now() - INTERVAL '1 hours')
                    group by 2 limit 1"""
        LOGGER.debug(query)
        query_result = execute_query_return_query_result(query=query)
        LOGGER.debug("Query Result: %s", query_result)
        if len(query_result):
            return_status = status.HTTP_200_OK
        else:
            return_status = status.HTTP_204_NO_CONTENT
        return Response(data=query_result, status=return_status)


class QuestionHighestVoteView(APIView):
    """

    """
    @staticmethod
    def get(self):
        """
        7. Across the entire application, which question has had the highest number of votes ever.
        """
        query = """ select max(a.upvote) as upvote,
                           q.question_text 
                    from question q 
                    join answer a on (q.id=a.question_id_id)  
                    group by 2 limit 1 """
        LOGGER.debug(query)
        query_result = execute_query_return_query_result(query=query)
        LOGGER.debug("Query Result: %s", query_result)
        if len(query_result):
            return_status = status.HTTP_200_OK
        else:
            return_status = status.HTTP_204_NO_CONTENT
        return Response(data=query_result, status=return_status)
