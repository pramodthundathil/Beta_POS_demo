from django.db import models
from Inventory.models import  *
from Home.models import Staff
from django.contrib.auth.models import User  

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True,blank=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    invoice_number = models.CharField(max_length=20, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(default=0)  # Set default to 0
    total_amount_before_discount = models.FloatField(default=0)  # Set default to 0
    total_tax = models.FloatField(default=0)
    payment_status1 = models.CharField(max_length=20, default='UNPAID', choices=(("UNPAID","UNPAID"),("PAID","PAID"),("PARTIALLY","PARTIALLY")))
    payment_status = models.BooleanField(default=False)
    discount = models.FloatField(default=0)
    bill_discount = models.FloatField(default=0)
    save_status = models.BooleanField(default=False)
    sales_man = models.ForeignKey(Staff,on_delete=models.SET_NULL, null=True, blank=True)

    payed_amount = models.FloatField(default=0)
    balance_amount = models.FloatField()


    def adjust_stock(self):
        # Loop through each OrderItem in the order and deduct stock
        # for item in self.orderitem_set.all():
        #     product = item.product
        #     if product.Number_of_stock >= item.quantity:
        #         product.Number_of_stock -= item.quantity
        #         product.save()
                
        #     else:
        #         raise ValueError(f"Not enough stock for product: {product.name}")

        for item in self.orderitem_set.all():
            product = item.product
            remaining_quantity = item.quantity

            # First, try to adjust stock from batches
            while remaining_quantity > 0:
                # Get the oldest non-expired batch
                batch = product.batches.filter(expiry_date__gt=timezone.now().date(), stock_quantity__gt=0).order_by('expiry_date').first()

                if not batch:
                    # If no more batches are available, break out and adjust stock from the product level
                    break

                if batch.stock_quantity >= remaining_quantity:
                    # If the batch has enough stock to fulfill the order
                    batch.stock_quantity -= remaining_quantity
                    batch.save()
                    remaining_quantity = 0
                else:
                    # If the batch doesn't have enough stock, use all its stock and move to the next batch
                    remaining_quantity -= batch.stock_quantity
                    batch.stock_quantity = 0
                    batch.save()
    

            if product.Number_of_stock >= item.quantity:
                product.Number_of_stock -= item.quantity
                product.save()
            else:
                raise ValueError(f"Not enough stock for product: {product.name}")


    def update_totals(self):
        total_amount_before_discount = 0
        total_amount = 0
        total_tax = 0
        total_discount = 0

        for item in self.orderitem_set.all():
            # Calculate the total amount before discount
            item_total_before_discount = item.unit_price * item.quantity
            total_amount_before_discount += item_total_before_discount
            
            # Sum up the discount for each item
            total_discount += item.discount

            # Calculate the total price (after discount) and total tax for each item
            total_amount += item.total_price  # `total_price` already includes the discount
            total_tax += item.total_tax
        
         # Apply bill_discount to the total discount
        total_discount += float(self.bill_discount)

    # Adjust the total amount by subtracting the bill discount
        total_amount -= float(self.bill_discount)

        self.total_amount_before_discount = total_amount_before_discount
        self.total_amount = total_amount  # Already discounted total amount
        self.total_tax = total_tax
        self.discount = total_discount # Set the order discount as the sum of item discounts
        self.save()
       
        
    def calculate_balance(self):
        # Calculate balance amount based on total, discount, and amount paid
        discounted_total = self.total_amount - self.discount
        self.balance_amount = discounted_total - self.payed_amount
        self.save()
        
    def save(self, *args, **kwargs):
        # Update balance amount before saving
        self.balance_amount = self.total_amount - self.payed_amount
        
        # Update payment status based on payed amount
        if self.payed_amount == 0:
            self.payment_status1 = 'UNPAID'
        elif self.payed_amount >= self.total_amount:
            self.payment_status1 = 'PAID'
        else:
            self.payment_status1 = 'PARTIALLY'
        
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.invoice_number} by {self.customer.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.FloatField()
    discount = models.FloatField(default=0)
    total_price = models.FloatField(editable=False)  # Make this field non-editable
    total_tax = models.FloatField(editable=False)  # Make this field non-editable


    # Example tax rate of 10%

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.unit_price  # Assuming the product has a price field
        self.total_price = self.unit_price * self.quantity - self.discount
        self.total_tax = self.product.tax_amount * self.quantity
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"

from django.core.exceptions import ValidationError


class  Returns(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    return_number = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)
    reason  = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    confirmation = models.BooleanField(default=False)
    adjustment = models.BooleanField(default=False)
    adjustment_comment = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate purchase order number if it doesn't exist
        if not self.return_number:
            self.return_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        # Loop to ensure uniqueness
        while True:
            random_number = random.randint(1000, 9999)  # 5-digit random number
            order_number = f"RT-{random_number}"
            if not Returns.objects.filter(return_number=order_number).exists():
                return order_number


class ReturnOrderItem(models.Model):
    return_number = models.ForeignKey(Returns, on_delete= models.CASCADE, related_name='returns')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="return_items")
    return_quantity = models.PositiveIntegerField()
    return_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True, null=True)  # Optional reason for return

    def clean(self):
        # Ensure return quantity does not exceed ordered quantity
        if self.return_quantity > self.order_item.quantity:
            raise ValidationError("Return quantity cannot exceed ordered quantity.")

    


