from django.db import models

class user(models.Model):
    user_name = models.CharField(max_length=50)
    user_image = models.ImageField(upload_to='photos/drink/drink_user/', blank=True)

    def __str__(self):
        return self.user_name

class Order(models.Model):
    order_name = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField()
    extra_amount = models.IntegerField()
    final_amount = models.IntegerField()

    def __str__(self):
        return self.order_name  

class orderdetail(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)  # xóa order thì xóa lun orderdetail
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)  
    drink_name = models.CharField(max_length=100, default='Unknown Drink')
    drink_image = models.ImageField(upload_to='photos/drink/drinks/', blank=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total = models.IntegerField()

