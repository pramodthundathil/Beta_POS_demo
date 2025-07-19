from django import forms
from .models import Product, Purchase, Vendor, Customer, InventoryStock, PurchaseOrder, Batch
from datetime import timezone


class InventoryStockForm(forms.ModelForm):
    class Meta:
        model = InventoryStock
        fields = [
            'product_name', 'product_stock', 'unit', 
            'min_stock_level', 'last_purchase_date', 
            'last_purchase_amount'
        ]
        
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'product_name', 'placeholder': 'Enter product name'}),
            'product_stock': forms.NumberInput(attrs={'class': 'form-control', 'id': 'product_stock', 'placeholder': 'Enter product stock', 'min': 0}),
            'unit': forms.Select(attrs={'class': 'form-control', 'id': 'unit', 'required': True}),
            'min_stock_level': forms.NumberInput(attrs={'class': 'form-control', 'id': 'min_stock_level', 'placeholder': 'Enter minimum stock level', 'min': 0}),
            'last_purchase_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'last_purchase_date', 'type': 'date'}),
            'last_purchase_amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'last_purchase_amount', 'placeholder': 'Enter last purchase amount', 'step': '0.01', 'min': 0}),
        }


# class PurchaseOrderForm(forms.ModelForm):
#     class Meta:
#         model = PurchaseOrder
#         fields = [
#             'purchase_type', 'valid_till', 'supplier', 'place_of_supply', 
#             'purchase_item', 'unit', 'quantity', 'purchase_price', 'discount', 'amount', 'order_status'
#         ]
        
#         widgets = {
#             'purchase_type': forms.Select(attrs={'class': 'form-control', 'id': 'purchase_type'}),
#             'valid_till': forms.DateTimeInput(attrs={'class': 'form-control', 'id': 'valid_till', 'type': 'date'}),
#             'supplier': forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
#             'place_of_supply': forms.TextInput(attrs={'class': 'form-control', 'id': 'place_of_supply', 'placeholder': 'Enter place of supply'}),
#             'purchase_item': forms.Select(attrs={'class': 'form-control', 'id': 'purchase_item'}),
#             'unit': forms.Select(attrs={'class': 'form-control', 'id': 'unit'}),
#             'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity', 'placeholder': 'Enter quantity', 'min': 0}),
#             'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'purchase_price', 'placeholder': 'Enter purchase price', 'step': '0.01', 'min': 0}),
#             'discount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'discount', 'placeholder': 'Enter discount (%)', 'step': '0.01', 'min': 0}),
#             'amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'amount', 'placeholder': 'Enter total amount', 'step': '0.01', 'min': 0}),
#             'order_status': forms.Select(attrs={'class': 'form-control', 'id': 'order_status'}),
#         }

from django.utils import timezone
class PurchaseForm(forms.ModelForm):
    
    class Meta:
        model = Purchase
        fields = [
            'purchase_type', 'supplier', 'payment_terms', 'due_date', 'place_of_supply',
            'purchase_item', 'quantity', 'purchase_price', 'discount', 'unit', 
            'amount', 'paid_amount', 'balance_amount', 'payment_status', 'shipping_cost', 'recived_date'
        ]
        labels = {
            'purchase_price':'Purchase Unit Price',
            "recived_date":'received Date'
        }
        widgets = {
            'purchase_type': forms.Select(attrs={'class': 'form-control', 'id': 'purchase_type'}),
            'supplier': forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
            'payment_terms': forms.TextInput(attrs={'class': 'form-control', 'id': 'payment_terms'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'due_date', 'type': 'date'}),
            'place_of_supply': forms.TextInput(attrs={'class': 'form-control', 'id': 'place_of_supply'}),
            'purchase_item': forms.Select(attrs={'class': 'form-control', 'id': 'purchase_item'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity', 'min': 0}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'purchase_price', 'step': '0.01', 'min': 0}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'discount', 'step': '0.01', 'min': 0}),
            'unit': forms.Select(attrs={'class': 'form-control', 'id': 'unit'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'amount', 'step': '0.01', 'min': 0}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'paid_amount', 'step': '0.01', 'min': 0}),
            'balance_amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'balance_amount', 'step': '0.01', 'min': 0}),
            'payment_status': forms.Select(attrs={'class': 'form-control', 'id': 'payment_status'}),
            'shipping_cost': forms.NumberInput(attrs={'class': 'form-control', 'id': 'shipping_cost', 'step': '0.01', 'min': 0}),
            'recived_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'recived_date', 'type': 'date','max': timezone.now().date()}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'inventory', 'unit_price', 'unit_quantity', 'unit', 'Number_of_stock',"barcode_number", 'description', 'tax', 'tax_value']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'category'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'inventory': forms.Select(attrs={'class': 'form-control', 'id': 'inventory'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'price', 'step': '0.01', 'min': 0, 'pattern': '\d+(\.\d{1,2})?'}),
            'unit_quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'unit_qantiry', 'step': '0.01', 'min': 0, 'pattern': '\d+(\.\d{1,2})?'}),
            'Number_of_stock': forms.NumberInput(attrs={'class': 'form-control', 'id': 'stock', 'min': 0}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'description', 'rows': 3}),
            'unit': forms.Select(attrs={'class': 'form-control', 'id': 'unit'}),
            'barcode_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'barcode_number'}),
            'tax': forms.Select(attrs={'class': 'form-control'}),
            'tax_value': forms.Select(attrs={'class': 'form-control'})
        }


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'email', 'phone_number', 'city', 'state', 'country', 'pincode', 'contact_info', 'supply_product']
        labels = {
            "pincode":"Location Url"
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'vendor_name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'vendor_email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'vendor_phone_number'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'vendor_city'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'id': 'vendor_state'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'id': 'vendor_country'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'id': 'vendor_pincode',"type":"url"}),
            'contact_info': forms.Textarea(attrs={'class': 'form-control', 'id': 'vendor_contact_info', 'rows': 3}),
            'supply_product': forms.TextInput(attrs={'class': 'form-control', 'id': 'vendor_supply_product'}),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'city', 'state', 'country', 'pincode', 'contact_info',"customer_photo"]
        labels = {
            "pincode":"Location Of Customer"
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'customer_name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'customer_phone', "type":"number"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'customer_email'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'customer_city'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'id': 'customer_state'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'id': 'customer_country'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'id': 'customer G-map Location', "type":"url"}),
            'contact_info': forms.Textarea(attrs={'class': 'form-control', 'id': 'customer_contact_info', 'rows': 3}),
            
        }


class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['product', 'expiry_date', 'stock_quantity', 'manufactured_date']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'id': 'batch-product'
            }),
            
            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'batch-expiry_date',
                'placeholder': 'YYYY-MM-DD',
                'type': 'date'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'batch-stock_quantity',
                'min': 0,
                'placeholder': 'Enter stock quantity'
            }),
            'manufactured_date': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'batch-manufactured_date',
                'placeholder': 'YYYY-MM-DD',
                'type': 'date'
            }),
        }

    