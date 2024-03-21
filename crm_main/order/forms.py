from django import forms
from .models import Order, OrderProduct

class AddOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # fields = ('name', 'email', 'description', 'priority', 'status',)
        fields = ('order_number', 'client', 'status','total','status',) # should eidt order date here.

# ======================================================
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_number', 'created_by', 'client', 'status', 'total', 'shipment_company', 'tracking_number', 'shiping_fee']
        widgets = {
            'order_number': forms.TextInput(attrs={'class': 'form-control'}),
            'created_by': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'shipment_company': forms.TextInput(attrs={'class': 'form-control'}),
            'tracking_number': forms.TextInput(attrs={'class': 'form-control'}),
            'shiping_fee': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'order_date': forms.NumberInput(attrs={'class': 'form-control'}),
        }
# this is used to create a formset for the OrderProduct model, it is used to create multiple OrderProduct objects at once.
# OrderProductFormSet = forms.inlineformset_factory(Order, OrderProduct, form=OrderProductForm, extra=1, can_delete=True) 