from .models import Order
from django import forms


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone_number', 'user',
                  ' reciver_address', ' reciver_name', 'reciver_phone_number']
