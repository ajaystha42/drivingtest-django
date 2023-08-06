from django.db import models
import random
import uuid
# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self) -> str:
        return "%s - %s - %s" % (self.id, self.username, self.name)

    class Meta:
        db_table = 'users'


class Category(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    category_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.category_name


class Question(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    category = models.ForeignKey(
        Category, related_name='category', on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    marks = models.IntegerField(default=5)

    def __str__(self) -> str:
        return self.question

    def get_answer(self):
        answer_objs = list(Answer.objects.filter(question=self))
        random.shuffle(answer_objs)
        data = []
        for answer_obj in answer_objs:
            data.append(
                {
                    'id': answer_obj.id,
                    'answer': answer_obj.answer,
                    'is_correct': answer_obj.is_correct
                }
            )
        return data


class Answer(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    question = models.ForeignKey(
        Question, related_name='question_answer', on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.answer
