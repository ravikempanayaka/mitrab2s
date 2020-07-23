import logging
import getpass
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Answer
from ..serializers import AnswerSerializer

LOGGER = logging.getLogger(__name__)


class AnswerView(APIView):
    """

    """

    def get(self, request):
        """

        :param request:
        :return:
        """
        anwser_data = None
        question_id = request.query_params['question_id']
        if question_id:
            anwser_data = Answer.objects.filter(question_id=question_id).values('answer_text')
            LOGGER.debug("Answer data are: %s", anwser_data)
            if anwser_data:
                return_status = status.HTTP_200_OK
            else:
                return_status = status.HTTP_400_BAD_REQUEST
        else:
            return_status = status.HTTP_400_BAD_REQUEST
        return Response(data=anwser_data, status=return_status)

    def post(self, request):
        """

        :param request:
        :return:
        """
        bad_request = False
        user_id = None
        question_id = None
        answer = None
        upvote = None
        return_dict = None
        LOGGER.debug("inside answer post method")
        LOGGER.debug("request data: %s", request.data)
        tracket_dict = {
            'create_user': getpass.getuser(),
            'create_program': __name__,
            'create_datetime': datetime.now(),
            'modify_user': getpass.getuser(),
            'modify_program': __name__,
            'modify_datetime': datetime.now()
        }
        if 'user_id' in request.data and request.data['user_id']:
            user_id = request.data['user_id']
            LOGGER.debug("user_id: %s", user_id)
        else:
            bad_request = True

        if 'question_id' in request.data and request.data['question_id']:
            question_id = request.data['question_id']
            LOGGER.debug("question id: %s", question_id)
        else:
            bad_request = True

        if 'answer' in request.data and request.data['answer']:
            answer = request.data['answer']
            LOGGER.debug("Answer: %s", answer)
        else:
            bad_request = True

        if 'upvote' in request.data and request.data['upvote']:
            upvote = request.data['upvote']
            LOGGER.debug("Upvote: %s", upvote)
        else:
            bad_request = True

        if bad_request:
            return_status = status.HTTP_400_BAD_REQUEST
        else:
            post_set = {
                'user_id': user_id,
                'question_id': question_id,
                'answer_text': answer,
                'upvote': upvote
            }
            post_set.update(tracket_dict)
            serializer = AnswerSerializer(data=post_set)
            if serializer.is_valid():
                serializer.save()
                return_dict = serializer.data
                return_status = status.HTTP_201_CREATED
            else:
                return_status = status.HTTP_400_BAD_REQUEST
        return Response(data=return_dict, status=return_status)

    def patch(self, request, **kwargs):
        """

        :param request:
        :return:
        update based an upvoted by user and based on question id
        """
        LOGGER.debug("inside answer patch method")
        question_id = None
        upvote = None
        return_status = None
        # user id get from kwargs or query_params now i take query params
        # user_id = self.kwargs['user_id']
        # LOGGER.debug("user_id: %s", user_id)
        user_id = request.query_params['user_id']

        if 'question_id' in request.query_params:
            question_id = request.query_params['question_id']
            LOGGER.debug("Question Id: %s", question_id)
        else:
            LOGGER.debug("question id not in the request so we consider from only user id")

        if user_id and question_id:
            answer_obj = Answer.objects.filter(user_id=user_id, question_id=question_id)

            if answer_obj:
                if 'upvote' in request.data['upvote']:
                    upvote = request.data['upvote']
                    LOGGER.debug("Upvote are: %s", upvote)
                    answer_obj.update(upvote=upvote,
                                      modify_datetime=datetime.now(),
                                      modify_program=__name__,
                                      modify_user=getpass.getuser())
                    return_status = status.HTTP_204_NO_CONTENT
                else:
                    LOGGER.debug("upvote not in the request")
            else:
                LOGGER.debug("user id and question id not match in table")
        else:
            answer_obj = Answer.objects.filter(user_id=user_id)

            if answer_obj:
                answer_obj.update(upvote=upvote,
                                  modify_datetime=datetime.now(),
                                  modify_program=__name__,
                                  modify_user=getpass.getuser())
                return_status = status.HTTP_204_NO_CONTENT
            else:
                LOGGER.debug("User ID not in the table")
                return_status = status.HTTP_400_BAD_REQUEST
        return Response(data=None, status=return_status)
