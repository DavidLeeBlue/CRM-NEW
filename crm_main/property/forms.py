from django import forms
from .models import Property, PropertyImage, PropertyComment, PropertyCommentImage

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('title', 'description', 'address',)

class PropertyImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = PropertyImage
        fields = ('image',)

class PropertyCommentForm(forms.ModelForm):
    class Meta:
        model = PropertyComment
        fields = ['content']

class PropertyCommentImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = PropertyCommentImage
        fields = ['image']