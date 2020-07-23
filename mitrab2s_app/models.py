from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


# Create your models here.
class Tracker(models.Model):
    create_datetime = models.DateTimeField(default=now, null=False, blank=False)
    create_user = models.CharField(max_length=50, null=False, blank=False)
    create_program = models.CharField(max_length=200, null=False, blank=False)
    modify_datetime = models.DateTimeField(default=now, null=False, blank=False)
    modify_user = models.CharField(max_length=50, null=False, blank=False)
    modify_program = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        abstract = True


class Question(Tracker):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200, null=False, blank=True)

    def __str__(self):
        return "%s | %s" % (self.question_text, self.user_id_id)

    class Meta:
        managed = True
        db_table = 'question'


class Answer(Tracker):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200, help_text="Write your text here ..")
    upvote = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return "%s | %s | %s | %s " % (self.answer_text, self.upvote, self.user_id_id, self.question_id_id)

    class Meta:
        managed = True
        db_table = 'answer'



