from django.db import models
import re
import bcrypt
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField



class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = " Last_name should be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):              
            errors['email'] = "Invalid email address!"
        
        if len(postData['password']) < 8:
            errors["password"] = " Password should be at least 8 characters"
        
        if postData['password'] != postData['confirm_PW']:
            errors['confirm_PW'] =  "Password does not match"     
        
        print(errors)
        return errors

    
    def login_validator(self, postData):
        errors = {}
        user_list_to_login = User.objects.filter(email=postData['login_email'])
        if len(user_list_to_login) == 0:
            errors['login_email'] = "There was a problem email"
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), user_list_to_login[0].password.encode()):
                erroes['login_password'] = "There was a problem password"
        
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Shipping(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    street = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zipcode = models.TextField()
    user = models.ForeignKey(User, related_name="shipping_info", on_delete = models.CASCADE)
    
class Billing(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    street = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zipcode = models.TextField()
    cc_number = CardNumberField()
    cc_expiry = CardExpiryField()
    cc_code = SecurityCodeField()
    user = models.ForeignKey(User, related_name="billing_info", on_delete = models.CASCADE)




class Order(models.Model):
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="orders", null = True, on_delete = models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping = models.ForeignKey(Shipping, related_name="orders", null = True, on_delete = models.SET_NULL)
    billing = models.ForeignKey(Billing, related_name="orders", null = True, on_delete = models.SET_NULL)

class Item(models.Model):
    category = models.CharField(max_length=255)
    Name = models.CharField(max_length=255)
    Desc = models.TextField()
    Front_pic = models.URLField(max_length=200)
    Back_pic =  models.URLField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order_item(models.Model):
    quantity = models.IntegerField()
    sub_total = models.DecimalField(max_digits=8, decimal_places=2)
    order = models.ForeignKey(Order, related_name="order_items", on_delete = models.CASCADE)
    item = models.ForeignKey(Item, related_name="order_items", on_delete = models.CASCADE )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class AdminManager(models.Manager):
    def admin_validator(self, postData):
        errors = {}
        user_list_to_login = User.objects.filter(email=postData['login_email'])
        if len(user_list_to_login) == 0:
            errors['login_email'] = "There was a problem email"
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), user_list_to_login[0].password.encode()):
                erroes['login_password'] = "There was a problem password"
        
        return errors

class Admin(models.Model):
    email =  models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AdminManager()
    
