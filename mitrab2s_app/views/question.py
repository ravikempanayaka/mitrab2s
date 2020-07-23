import logging
import json
import getpass
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Question, Answer
from ..utils.utils import execute_query_return_query_result
from ..serializers import QuestionSerializer

LOGGER = logging.getLogger(__name__)


class QuestionView(APIView):
    """

    """
    template_name = 'index.html'

    @staticmethod
    def get(request):
        """

        :param request:
        :return:
        """
        data = None
        question_id = None
        user_id = request.query_params['user_id']
        if 'question_id' in request.query_params:
            question_id = request.query_params['question_id']
            LOGGER.debug("Question Id: %s", question_id)
        else:
            LOGGER.debug("question id not in the request")

        if user_id and question_id:

            data = Question.objects.filter(user_id=user_id,
                                           id=question_id).values('question_text')
            LOGGER.debug("data: %s", data)
            if len(data):
                return_status = status.HTTP_200_OK
            else:
                return_status = status.HTTP_400_BAD_REQUEST
        elif user_id:
            data = Question.objects.filter(user_id=user_id).values('question_text')
            LOGGER.debug("data: %s", data)
            if len(data):
                return_status = status.HTTP_200_OK
            else:
                return_status = status.HTTP_400_BAD_REQUEST
        else:
            return_status = status.HTTP_400_BAD_REQUEST
        return Response(data=data, status=return_status)

    def post(self, request, **kwargs):
        """

        :param request:
        :return:
        """
        LOGGER.debug("inside question post method")
        return_status = None
        bad_request = False
        question_text = None
        return_dict = None
        # user id get from kwargs or query_params now i take query params

        # user_id = self.kwargs['user_id']
        # LOGGER.debug("User ID: %s", user_id)
        user_id = request.query_params['user_id']
        tracket_dict = {
            'create_user': getpass.getuser(),
            'create_program': __name__,
            'create_datetime': datetime.now(),
            'modify_user': getpass.getuser(),
            'modify_program': __name__,
            'modify_datetime': datetime.now()
        }
        if 'question_text' in request.data and request.data['question_text']:
            question_text = request.data['question_text']
            LOGGER.debug("Question Text: %s", question_text)
        else:
            bad_request = True
        if bad_request:
            return_status = status.HTTP_400_BAD_REQUEST
        else:
            post_set = {
                'user_id': user_id,
                'question_text': question_text
            }
            post_set.update(tracket_dict)
            serializer = QuestionSerializer(data=post_set)
            if serializer.is_valid():
                serializer.save()
                return_dict = serializer.data
            else:
                LOGGER.debug("serializer not valid")
                return_status = status.HTTP_400_BAD_REQUEST
        return Response(data=return_dict, status=return_status)

    def patch(self, request, **kwargs):
        """

        :param request:
        :param kwargs:
        :return:
        """
        LOGGER.debug("Inside question patch method")
        question_text = None
        # user id get from kwargs or query_params now i take query params
        # user_id = self.kwargs['user_id']
        # LOGGER.debug("User ID: %s", user_id)

        user_id = request.query_params['user_id']

        if 'question_id' in request.query_params:
            question_id = request.query_params['question_id']
            print("question Id: ", question_id)
            LOGGER.debug("Question Id: %s", question_id)
        else:
            return_dict = {
                'message': "question id is required for update process",
                "status_code": status.HTTP_400_BAD_REQUEST
            }
            return Response(data=return_dict, status=status.HTTP_400_BAD_REQUEST)

        if 'question_text' in request.data and request.data['question_text']:
            question_text = request.data['question_text']
            print("question text: ", question_text)
            LOGGER.debug("question text: %s", question_text)

        if user_id and question_text:
            question_obj = Question.objects.filter(user_id=user_id).update(question_text=question_text,
                                                                           modify_datetime=datetime.now(),
                                                                           modify_program=__name__,
                                                                           modify_user=getpass.getuser())
            LOGGER.debug("Question update are: %s", question_obj)
            return_status = status.HTTP_204_NO_CONTENT
        else:
            return_status = status.HTTP_400_BAD_REQUEST
        return Response(data=None, status=return_status)