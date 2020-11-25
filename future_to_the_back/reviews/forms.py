from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):

    rate = forms.FloatField(min_value=0.0, max_value=10.0)
    
    class Meta:
        model = Review
        fields = ('title', 'photo','content','rate')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
