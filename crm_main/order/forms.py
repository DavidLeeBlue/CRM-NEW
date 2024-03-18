from django import forms
from .models import Order

class AddOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # fields = ('name', 'email', 'description', 'priority', 'status',)
        fields = ('order_number', 'client', 'status','total','status',) # should eidt order date here.