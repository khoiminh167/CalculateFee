
from django import forms
from django.core.exceptions import ValidationError
from .models import user, Order, orderdetail
from django.utils.translation import gettext as _
from django.forms import modelformset_factory


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = orderdetail
        fields = '__all__'
        exclude = ['total']

    def __init__(self, *args, **kwargs):
        super(CreateOrderForm, self).__init__(*args, **kwargs)

        # Correct label names
        self.fields['order_id'].label = _('Đơn hàng')
        self.fields['user_id'].label = _('Người đặt')
        self.fields['drink_name'].label = _('Tên món')
        self.fields['drink_image'].label = _('Hình ảnh (nếu có)')
        self.fields['quantity'].label = _('Số lượng')
        self.fields['price'].label = _('Đơn giá')


    def clean(self):
        cleaned_data = super().clean()
        # add validation logic ở đây
        return cleaned_data
    
class CreateUserForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ['user_name', 'user_image'] 


class CreateMainOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['total_amount','final_amount','extra_amount']

    def __init__(self, *args, **kwargs):
        super(CreateMainOrderForm, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()
        # add validation logic ở đây
        return cleaned_data
    

    
class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['total_amount','final_amount']

    def __init__(self, *args, **kwargs):
        super(UpdateOrderForm, self).__init__(*args, **kwargs) 
        self.fields['total_amount'].label = _('Nhập số tiền ban đầu')

        self.fields['final_amount'].label = _('Nhập số tiền sau giảm')