from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        # db_table = ''
        # managed = True
        # verbose_name = 'ModelName'
        # verbose_name_plural = 'ModelNames'
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name": "Your name",
            "user_email": "Your email",
            "text": "Your comment"
        }
        # error_messages = {
        #     "user_name": {
        #         "required": "Your name must not be empty!",
        #         "max_length": "Please enter a shsorter name!"
        #     }
        # }
