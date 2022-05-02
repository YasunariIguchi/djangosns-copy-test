from django import forms

from .models import Community, CommunityPost

class CommunityCreateForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = (
            'name','memo'
        )
        labels={
            'name':'コミュニティ名',
            'memo':'コミュニティの説明',
            }

class CommunityPostCreateForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = (
            'content',
        )
        widgets = {
            'content': forms.Textarea(
                attrs={'rows': 3, 'cols': 50, 'placeholder': 'ここに入力'}
            ),
        }
        labels={
            'content':'投稿内容',
            }