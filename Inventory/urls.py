from django.urls import path, include
from .import views 
from .api import api_views
from django.urls import path 
# serializer view__________________________________

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




urlpatterns = [
    #units management ...............................
    path("list_units",views.list_units,name="list_units"),
    path('add_unit/', views.add_unit, name='add_unit'),
    path('update_unit/<int:unit_id>/', views.update_unit, name='update_unit'),
    path("delete_unit/<int:pk>",views.delete_unit,name="delete_unit"),

    # vendor management ......................................

    path("add_vendor",views.add_vendor,name="add_vendor"),
    path("list_vendor",views.list_vendor,name="list_vendor"),
    path("update_vendor/<int:pk>",views.update_vendor,name="update_vendor"),
    path("delete_vendor/<int:pk>",views.delete_vendor,name="delete_vendor"),

    # inventory management ....................................

    path("add_inventory",views.add_inventory,name="add_inventory"),
    path("edit_inventory/<int:pk>",views.edit_inventory,name="edit_inventory"),
    path("delete_inventory/<int:pk>",views.delete_inventory,name="delete_inventory"),
    path("list_inventory",views.list_inventory,name="list_inventory"),
    path("delete_category/<int:pk>",views.delete_category,name="delete_category"),



    # purchase order handing ..............................
    path("add_purchase_order",views.add_purchase_order,name="add_purchase_order"),
    path("list_purchase_order",views.list_purchase_order,name="list_purchase_order"),
    path("purchase_order_invoice/<int:pk>",views.purchase_order_invoice,name="purchase_order_invoice"),
    path("edit_purchase_order/<int:pk>",views.edit_purchase_order,name="edit_purchase_order"),
    path("add_purchase_order_item/<int:pk>",views.add_purchase_order_item,name="add_purchase_order_item"),
    path("update_purchase_order_item/<int:order_id>",views.update_purchase_order_item,name="update_purchase_order_item"),
    path("update_supplier_to_purchase_order",views.update_supplier_to_purchase_order,name="update_supplier_to_purchase_order"),
    path("change_purchase_order_date/<int:pk>",views.change_purchase_order_date,name="change_purchase_order_date"),
    path("delete_purchase_order/<int:pk>",views.delete_purchase_order,name="delete_purchase_order"),
    path("delete_purchase_order_item/<int:pk>",views.delete_purchase_order_item,name="delete_purchase_order_item"),

    # ###### purchases....................

    path("purchase",views.purchase,name="purchase"),
    path("add_purchase",views.add_purchase,name="add_purchase"),
    path("purchase_from_order/<int:order_id>",views.purchase_from_order,name="purchase_from_order"),
    path("edit_purchase/<int:pk>",views.edit_purchase,name="edit_purchase"),
    path("deletepurchase/<int:pk>",views.deletepurchase,name="deletepurchase"),
    path("change_purchase_date/<int:pk>",views.change_purchase_date,name="change_purchase_date"),
    path("add_purchase_item/<int:pk>",views.add_purchase_item,name="add_purchase_item"),
    path("update_supplier_to_purchase",views.update_supplier_to_purchase,name="update_supplier_to_purchase"),
    path("update_purchase_item/<int:order_id>",views.update_purchase_item,name="update_purchase_item"),
    path("update_purchase_payment/<int:order_id>",views.update_purchase_payment,name="update_purchase_payment"),
    path("payment_given_in_expense_purchase",views.payment_given_in_expense_purchase,name="payment_given_in_expense_purchase"),
    path("add_bill_discount_to_purchase/<int:pk>",views.add_bill_discount_to_purchase,name="add_bill_discount_to_purchase"),
    path("delete_purchase_item/<int:pk>",views.delete_purchase_item,name="delete_purchase_item"),


    #data import 

    path("import_data_from_excel_inventory",views.import_data_from_excel_inventory,name="import_data_from_excel_inventory"),
    
    #product management........................................

    path('add-category/', views.add_category, name='add_category'),
    path("list_category/",views.list_category,name="list_category"),
    path("list_products",views.list_products,name="list_products"),
    path("add_product",views.add_product,name="add_product"),
    path("create_batch/<int:product_id>",views.create_batch,name="create_batch"),
    path("update_batch/<int:pk>",views.update_batch,name="update_batch"),

    #barcodes

    path("product_barcode_image/<int:pk>",views.product_barcode_image,name="product_barcode_image"),
    path("barcode_view/<int:pk>",views.barcode_view,name="barcode_view"),
    

    path("disable_product/<int:pk>",views.disable_product,name="disable_product"),
    path("product_update/<int:product_id>",views.product_update,name="product_update"),
    path("incresse_product_stock/<int:product_id>",views.incresse_product_stock,name="incresse_product_stock"),
    path("decrease_product_stock/<int:product_id>",views.decrease_product_stock,name="decrease_product_stock"),
    path("delete_product/<int:pk>",views.delete_product,name="delete_product"),
    path('AddTax', views.AddTax, name='AddTax'),
    path('ListTax', views.ListTax, name='ListTax'),

    path("add_customer/<int:pk>",views.add_customer,name="add_customer"),
    path("list_customer",views.list_customer,name="list_customer"),
    path("add_customers",views.add_customers,name="add_customers"),
    path("delete_customer/<int:pk>",views.delete_customer,name="delete_customer"),
    path("update_customer/<int:pk>",views.update_customer,name="update_customer"),

    #bulk delete

    path("delete_bulk_inventory",views.delete_bulk_inventory,name="delete_bulk_inventory"),
    path("delete_bulk_purchase",views.delete_bulk_purchase,name="delete_bulk_purchase"),
    path("delete_bulk_purchase_order",views.delete_bulk_purchase_order,name="delete_bulk_purchase_order"),
    path("delete_bulk_products",views.delete_bulk_products,name="delete_bulk_products"),
    path("delete_bulk_invoice",views.delete_bulk_invoice,name="delete_bulk_invoice"),
    path("delete_bulk_invoice_partial",views.delete_bulk_invoice_partial,name="delete_bulk_invoice_partial"),
    path("delete_bulk_invoice_pending",views.delete_bulk_invoice_pending,name="delete_bulk_invoice_pending"),
    path("delete_bulk_income",views.delete_bulk_income,name="delete_bulk_income"),
    path("delete_bulk_expense",views.delete_bulk_expense,name="delete_bulk_expense"),
    path("delete_bulk_category",views.delete_bulk_category,name="delete_bulk_category"),
    path("delete_bulk_supplier",views.delete_bulk_supplier,name="delete_bulk_supplier"),
    path("delete_bulk_customers",views.delete_bulk_customers,name="delete_bulk_customers"),
    path("delete_bulk_staff",views.delete_bulk_staff,name="delete_bulk_staff"),
    path("delete_bulk_staff_salary",views.delete_bulk_staff_salary,name="delete_bulk_staff_salary"),

   
    #api datas

    path("product_list",api_views.product_list,name="product_list"),
    path("product_detail/<int:pk>",api_views.product_detail,name="product_detail"),
    path("product_add",api_views.product_add,name="product_add"),
    path("product_add_new",api_views.ProductListCreateView.as_view(),name="product_add_new"),

]

urlpatterns += [
    path('api/token/', api_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
