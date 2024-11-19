from django.shortcuts import render, redirect,get_object_or_404
from django.views import View,generic
from django.contrib import messages
from .forms import CreateOrderForm, CreateUserForm ,CreateMainOrderForm,UpdateOrderForm
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect,HttpResponse
from .models import Order 
from django.views.generic.edit import FormMixin
from fillpdf import fillpdfs
import os


# Create your views here.
from calculateFee.models import user, Order, orderdetail

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'calculatefee/order_list.html', {'orders': orders})



class OrderCreateView(generic.CreateView):
    model = orderdetail  
    template_name = 'calculatefee/create_order_detail.html'
    form_class = CreateOrderForm
    context_object_name = 'orders'
    success_message = _("Create user order Successfully")
    
    def get_success_url(self):
        return reverse_lazy('calculateFee:order_view', kwargs={'pk': self.object.order_id.id})

    def form_valid(self, form):
        form.instance.total = 0
        response = super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_initial(self):
        initial = super().get_initial()
        order_id = self.kwargs.get('order_id') #get orderid từ url
        if order_id:
            initial['order_id'] = order_id
        return initial
    


class MainOrderCreateView(generic.CreateView):
    model = Order  
    template_name = 'calculatefee/create_order.html'
    form_class = CreateMainOrderForm
    context_object_name = 'orders'
    success_message = _("Create user order Successfully")
    def get_success_url(self):
        return reverse_lazy('calculateFee:order_view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.total_amount = 0
        form.instance.final_amount = 0
        form.instance.extra_amount = 0
        response = super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())
    

# Sử dụng get_context_data nếu bạn muốn tính toán và hiển thị kết quả trước khi người dùng gửi biểu mẫu.
# sử dụng form_valid nếu bạn muốn thực hiện tính toán và lưu kết quả sau khi người dùng gửi biểu mẫu.
class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = 'calculatefee/order_view.html'
    context_object_name = 'order'
    form_class = UpdateOrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_details'] = orderdetail.objects.filter(order_id=self.object.id)

        # Calculate sum of order detail prices
        sum_order_detail_prices = sum(detail.price for detail in context['order_details'])
        context['sum_order_detail_prices'] = sum_order_detail_prices

        # Add form to context
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.object)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)

        # Check if form is valid
        if form.is_valid():
            # Update `total_amount` and `final_amount` from form
            order_total_amount = form.cleaned_data.get('total_amount')
            order_final_amount = form.cleaned_data.get('final_amount')

            # Calculate extra_amount
            sum_order_detail_prices = sum(detail.price for detail in self.object.orderdetail_set.all())
            extra_amount = order_total_amount - sum_order_detail_prices

            # Update total amount and extra amount in the `order` object
            self.object.total_amount = order_total_amount
            self.object.final_amount = order_final_amount
            self.object.extra_amount = extra_amount
            self.object.save()

            # If total amount and final amount are valid, recalculate details
            if order_total_amount > 0 and order_final_amount > 0:
                for order_detail in self.object.orderdetail_set.all():
                    user_bill_percent = (order_detail.price / order_total_amount) * 100
                    order_detail.total = (user_bill_percent / 100) * order_final_amount
                    order_detail.save()

            form.save()  # Save the form
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('calculateFee:order_view', kwargs={'pk': self.object.pk})
    


def export_to_pdf(request, order_id):
    # Fetch the order object from the database
    order = get_object_or_404(Order, id=order_id)  # Sửa lại tên model là 'Order'

    # Define the path to the PDF template
    pdf_template_path = 'webmk/templates/pdf/order_receipt.pdf'

    # Define the data to fill in the PDF
    data_dict = {
        'order_id': order.id,
        'order_name': order.order_name,
        'created_date': order.created_date.strftime('%Y-%m-%d'),
        'total_amount': order.total_amount,
        'final_amount': order.final_amount,
        # Add more fields as necessary
    }

    # Fill the PDF
    filled_pdf_path = 'path/to/save/filled_pdf.pdf'
    fillpdfs.write_fillable_pdf(pdf_template_path, filled_pdf_path, data_dict)

    # Flatten the PDF (optional)
    fillpdfs.flatten_pdf(filled_pdf_path, filled_pdf_path)

    # Serve the PDF as a response
    with open(filled_pdf_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="order_{order.id}.pdf"'
        return response