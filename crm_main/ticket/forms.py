from django import forms
from .models import Ticket, Comment, TicketImage

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority', 'status',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = ('content',)
        fields = ['content', 'image']


# forms.py
# class TicketForm(forms.ModelForm):
#     images = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)

#     class Meta:
#         model = Ticket
#         fields = ('title', 'description', 'priority', 'status', 'images',)
        

        
# forms.py
class TicketImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = TicketImage
        fields = ('image',)