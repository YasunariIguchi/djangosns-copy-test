from django import forms

from .models import Community, CommunityPost

class CommunityCreateForm(forms.Form):
    name = forms.CharField(max_length=50, label = 'コミュニティ名')
    memo = forms.CharField(max_length=500, label = 'コミュニティの説明')
    #lat = forms.FloatField(initial=135.495734, label = 'x座標')
    #lon = forms.FloatField(initial=34.700559, label = 'y座標')
    zip21 = forms.RegexField(
        regex=r'^[0-9]+$',
        max_length=3,
    )
    zip22 = forms.RegexField(
        regex=r'^[0-9]+$',
        max_length=4,
        widget=forms.TextInput(attrs={'onKeyUp': "AjaxZip3.zip2addr('zip21','zip22','addr21','addr21')"}),
    )
    addr21 = forms.CharField(max_length=100, label = '住所')

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