from django import forms
from django.core.validators import FileExtensionValidator
from cobo.models import Question, Answer

class QuestionForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    )
    
    class Meta:
        model = Question
        fields = ['subject', 'content', 'image']
        labels = {
            'subject': '제목',
            'content': '내용',
            'image': '이미지',
        }

class AnswerForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    )
    
    class Meta:
        model = Answer
        fields = ['content', 'image']
        labels = {
            'content': '답변내용',
            'image': '이미지',
        }
