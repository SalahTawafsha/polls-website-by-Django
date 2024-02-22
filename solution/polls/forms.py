from django import forms


class QuestionForm(forms.Form):
    """ Form for creating a new question. """
    question_text = forms.CharField(label="Question", max_length=200)
