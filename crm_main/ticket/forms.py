from django import forms
from .models import Ticket, Comment, TicketImage, CommentImage

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority', 'status',)
        
# forms.py
class TicketImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = TicketImage
        fields = ('image',)

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         # fields = ('content',)
#         fields = ['content', 'image']

# 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
# forms.py
class CommentImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = CommentImage
        fields = ['image']

# forms.py
# class TicketForm(forms.ModelForm):
#     images = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)

#     class Meta:
#         model = Ticket
#         fields = ('title', 'description', 'priority', 'status', 'images',)
        

        
