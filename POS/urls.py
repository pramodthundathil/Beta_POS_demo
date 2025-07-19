from django.urls import path 
from .import views  



urlpatterns = [

    path("POS/<int:pk>",views.POS,name="POS"),
    path("search_product",views.search_product,name="search_product"),
    path("CreateOrder",views.CreateOrder,name="CreateOrder"),
    path("list_sale",views.list_sale,name="list_sale"),
    path("list_sale_pending",views.list_sale_pending,name="list_sale_pending"),
    path("list_sale_partial",views.list_sale_partial,name="list_sale_partial"),
    path("update_order",views.update_order,name="update_order"),
    path('update_order_customer',views.update_order_customer, name='update_order_customer'),
    path('update_order_salesman',views.update_order_salesman, name='update_order_salesman'),
    path('add_order_item/<int:pk>', views.add_order_item, name='add_order_item'),
    path('update_order_item_quantity', views.update_order_item_quantity, name='update_order_item_quantity'),
    path('update_order_payment/<int:order_id>/', views.update_order_payment, name='update_order_payment'),
    path("invoice/<int:pk>",views.invoice,name="invoice"),
    # path('update_order_payment/<int:order_id>/', views.update_order_payment, name='update_order_payment'),
    path("AddDiscount",views.AddDiscount,name="AddDiscount"),
    path("Listdiscount",views.Listdiscount,name="Listdiscount"),
    path('update_order_item/<int:order_id>/', views.update_order_item, name='update_order_item'),
    path("save_order/<int:order_id>",views.save_order,name="save_order"),
    path("add_product_from_order/<int:pk>",views.add_product_from_order,name="add_product_from_order"),
    path("change_invoice_date/<int:pk>",views.change_invoice_date,name="change_invoice_date"),

    # add diacount 

    path("add_bill_discount_to_order/<int:pk>",views.add_bill_discount_to_order,name="add_bill_discount_to_order"),
    

    
# delete invoice

    path("delete_invoice/<int:pk>",views.delete_invoice,name="delete_invoice"),
    path("delete_invoice_partial/<int:pk>",views.delete_invoice_partial,name="delete_invoice_partial"),
    path("delete_invoice_pending/<int:pk>",views.delete_invoice_pending,name="delete_invoice_pending"),
    path("delete_bulk_return",views.delete_bulk_return,name="delete_bulk_return"),



# returns 

    path("list_returns",views.list_returns,name="list_returns"),
    path("add_returns",views.add_returns,name="add_returns"),
    path("fetch_order_items",views.fetch_order_items,name="fetch_order_items"),
    path("create_return_on_purchase",views.create_return_on_purchase,name="create_return_on_purchase"),
    path("create_return_on_purchase/<int:pk>/<int:item_id>",views.create_return_on_purchase, name="create_return_on_purchase"),
    path("single_returns/<int:pk>",views.single_returns,name="single_returns"),
    path("ItemPOST/<int:pk>/<int:item_id>",views.ItemPOST, name="ItemPOST"),
    
    


    
]