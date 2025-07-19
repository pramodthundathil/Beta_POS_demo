from django.shortcuts import render, redirect, get_object_or_404
from Inventory.models import *
from django.http import JsonResponse
from datetime import datetime
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Finance.models import Income, Expence
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from Inventory.forms import ProductForm
from django.db import transaction



# Create your views here.

def generate_serial_number():
    with transaction.atomic():
        # Get the latest order based on ID to find the last invoice number
        last_order = Order.objects.order_by('-id').first()
        
        if last_order and last_order.invoice_number.startswith("SI-"):
            # Extract the numeric part, increment it, and format it with leading zeros
            last_number = int(last_order.invoice_number.split("-")[1])
            new_number = str(last_number + 1).zfill(5)  # Ensures it's 5 digits
        else:
            # Start from "SI-00001" if no previous order exists
            new_number = "00001"
        
        return f"SI-{new_number}"


@login_required(login_url='SignIn')
def CreateOrder(request):
    TokenU = generate_serial_number()

    order = Order.objects.create(invoice_number=TokenU)
    order.save()

    return redirect(POS,pk = order.id)
     

@login_required(login_url='SignIn')
def POS(request,pk):
    customer = Customer.objects.all()
    order = Order.objects.get(id = pk)
    product = Product.objects.all()
    invoice = Order.objects.all().order_by('-id')[:6]
    salesmans = Staff.objects.filter(designation = "Sales Man")
    product_form = ProductForm()

    context = {
        "customer":customer,
        "order":order,
        'product':product,
        "invoice":invoice,
        "salesmans":salesmans,
        'product_form':product_form
    }
    return render(request,'pos.html',context)

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def search_product(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'search' in request.GET:
        query = request.GET.get('search', '')
        products = Product.objects.filter(name__icontains=query, status=True)
        product_list = [{
            'name': product.name,
            'price': product.price,
            'tax': product.tax_amount,
            'stock': product.stock,
        } for product in products]
        return JsonResponse({'products': product_list})
    return JsonResponse({'products': []})


@login_required(login_url='SignIn')
def add_product_from_order(request,pk):
    if request.method == "POST":
        form = ProductForm(request.POST)
        ex_date = request.POST.get("ex_date")
        man_date = request.POST.get("man_date")
        order = Order.objects.get(id = pk)
        if form.is_valid():
            product = form.save()
            product.save()
            try:
                batch = Batch(
                    product = product,
                    expiry_date = ex_date,
                    manufactured_date = man_date,
                    stock_quantity = product.Number_of_stock
                )
                batch.save()
            except:
                batch = Batch(
                    product = product,
                    stock_quantity = product.Number_of_stock
                )
                batch.save()
            inventory = product.inventory  # Get the linked inventory
            try:
            # Fetch the number of units added from the form
                units_to_add = product.Number_of_stock

                # Calculate the total increase in stock based on product's unit_quantity
                total_increase = units_to_add * product.unit_quantity
                print(total_increase,"------------------------------------------------")  # For example, 100g * 10 = 1000g
                
                # Convert the total increase to kilograms if inventory is in kg
                if inventory.unit == 'kg':
                    total_increase_kg = total_increase / 1000  # Convert grams to kilograms
                    inventory.reduce_stock(total_increase_kg)  # Reduce inventory stock by this amount
                else:
                    # If the inventory unit is in grams, reduce directly
                    inventory.reduce_stock(total_increase)

                inventory.save()
        
            except (ValueError, KeyError):
                messages.error(request, "Invalid input. Please enter a valid stock number.")

            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            if not created:
                order_item.quantity += 1
                order_item.save()
            # Update order totals
            order.update_totals()

    return redirect('POS',pk=pk)


@login_required(login_url='SignIn')
@csrf_exempt
def update_order(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        order_id = request.POST.get('order_id')
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            # Assuming you have a way to get the current order, e.g., through session or context
            order = Order.objects.get(id = order_id)
            order.customer = customer
            order.save()
            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)


@login_required(login_url='SignIn')
@csrf_exempt
def update_order_customer(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            customer = Customer.objects.get(id=customer_id)
            order.customer = customer
            order.save()
            customer_details_html = render_to_string('ajaxtemplates/customerdetailsonpos.html', {'customers': customer,"order" : order})
            print(customer_details_html)
            return JsonResponse({"success": True, "html": customer_details_html})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Customer.DoesNotExist:
            return JsonResponse({"success": False, "error": "Customer not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required(login_url='SignIn')
@csrf_exempt
def update_order_salesman(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            customer = Staff.objects.get(id=customer_id)
            order.sales_man = customer
            order.save()
            customer_details_html = render_to_string('ajaxtemplates/customerdetailsonpos.html', {'customers': customer,"order" : order})
            print(customer_details_html)
            return JsonResponse({"success": True, "html": customer_details_html})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Customer.DoesNotExist:
            return JsonResponse({"success": False, "error": "Customer not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})



@login_required(login_url='SignIn')
def AddItemsToorder(request):
     return redirect('POS',pk=10)



@login_required(login_url='SignIn')
def list_sale(request):
    order = Order.objects.all().order_by('-order_date')

    context = {
         "order":order
    }
    return render(request,'list-sale.html',context)


@login_required(login_url='SignIn')
def list_sale_pending(request):
    order = Order.objects.filter(payment_status1 = "UNPAID" ).order_by('-order_date')

    context = {
         "order":order
    }
    return render(request,'list-sale-pending.html',context)

@login_required(login_url='SignIn')
def list_sale_partial(request):
    order = Order.objects.filter(payment_status1 = "PARTIALLY" ).order_by('-order_date')

    context = {
         "order":order
    }
    return render(request,'list-sale-partial.html',context)

def delete_invoice(request,pk):
    order = get_object_or_404(Order,id = pk)
    order.delete()
    messages.success(request,"Invoice Deleted.....")
    return redirect("list_sale")

def delete_invoice_partial(request,pk):
    order = get_object_or_404(Order,id = pk)
    order.delete()
    messages.success(request,"Invoice Deleted.....")
    return redirect("list_sale_partial")

def delete_invoice_pending(request,pk):
    order = get_object_or_404(Order,id = pk)
    order.delete()
    messages.success(request,"Invoice Deleted.....")
    return redirect("list_sale_pending")

def delete_bulk_return(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('contact_id[]')  # Get the selected IDs from the form
        print(selected_ids,"----------------------------------")
        if selected_ids:
            Returns.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'Selected items have been deleted.')
        else:
            messages.warning(request, 'No items were selected for deletion.')
    return redirect("list_returns")



@login_required(login_url='SignIn')
@csrf_exempt
def add_order_item(request,pk):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        print(product_id,")))))))))))))))))))))))))))))))))))))))))))")
        try:
            order = Order.objects.get(id=pk)
            if order.save_status == True:
                return JsonResponse({"success": False, "error": "Cannot Be added New Item to This order"})
            product = Product.objects.get(id=product_id)
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            if not created:
                order_item.quantity += 1
                order_item.save()
            
            # Update order totals
            order.update_totals()
            
            # Render the order items table
            order_items_html = render_to_string('ajaxtemplates/order_items_table.html', {'order': order})
            return JsonResponse({"success": True, "html": order_items_html,"order_item_id":f"#unit_price{order_item.id}"})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required(login_url='SignIn')
@csrf_exempt
def update_order_item(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        if order.save_status == False:
            item_id = request.POST.get('item_id')
            unit_price = float(request.POST.get('unit_price', 0))
            print(unit_price,"--------------------")
            discount = float(request.POST.get('discount', 0))
            quantity = int(request.POST.get('quantity', 1))
             

            # Find the OrderItem to update
            order_item = get_object_or_404(OrderItem, id=item_id, order=order)

            if quantity > order_item.product.Number_of_stock:
                return JsonResponse({"success": False, "error": "Product Stock exceeded"})


            # Update the OrderItem fields
            order_item.unit_price = unit_price
            order_item.discount = discount
            order_item.quantity = quantity
            order_item.save()  # This will also update the total_price based on save() logic
        try:
        # Update order totals
            order.update_totals()
            order.calculate_balance()

        # Prepare the updated data to return as a JSON response
            return JsonResponse({
                'success': True,
                'total_amount': order.total_amount,
                'balance_amount': order.balance_amount,
                'payment_status': order.payment_status1
            })
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required(login_url='SignIn')
@csrf_exempt
def update_order_item_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        try:
            order_item = OrderItem.objects.get(id=item_id)
            order = order_item.order
            order_item.delete()

            # Update order totals
            order_item.order.update_totals()

            # Render the order items table
            order_items_html = render_to_string('ajaxtemplates/order_items_table.html', {'order': order})
            return JsonResponse({"success": True, "html": order_items_html})
        except OrderItem.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order item not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


@csrf_exempt
def update_order_payment(request, order_id):
    if request.method == 'POST':
        payed_amount = float(request.POST.get('payed_amount'))
        discount = float(request.POST.get('discount'))
        
        try:
            order = Order.objects.get(id=order_id)    
            order.payed_amount = payed_amount
            order.balance_amount = order.total_amount - payed_amount

            
                        
            if payed_amount == 0:
                order.payment_status1 = 'UNPAID'
            elif payed_amount >= order.total_amount:
                order.payment_status1 = 'PAID'
            else:
                order.payment_status1 = 'PARTIALLY'
                
            order.save()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required(login_url='SignIn')
@csrf_exempt
def add_bill_discount_to_order(request,pk):
    order = Order.objects.get(id = pk)
    if request.method == "POST":
        discount = request.POST["bill_discount"]
        order.bill_discount = discount
        order.save()
        order.update_totals()
        order.calculate_balance()
        messages.success(request,"Discount Added.....")
        return redirect("POS",pk = pk)



@login_required(login_url='SignIn')
def save_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    previous_paid_amount = order.payed_amount
    # Save the order and calculate totals
    order.update_totals()
    order.calculate_balance()
    new_payedamount =  order.payed_amount - previous_paid_amount
    print(new_payedamount,"----------------------------------------")
    if Income.objects.filter(bill_number = order.invoice_number).exists():
        expense = Income.objects.filter(bill_number = order.invoice_number)
        total = 0
        
        for ex in expense:
            total = total + ex.amount
        
        amount = order.payed_amount - total
        if amount > 0:
            expense = Income(
                perticulers = f"Amount Against order {order.invoice_number}",
                amount =  round(amount, 2),
                bill_number = order.invoice_number,
                other = order.customer.name if order.customer else 'Cash Customer'
            
            )
        
            expense.save() 
    else:
        if order.payed_amount > 0:
            expense = Income(
                    perticulers = f"Amount Against order {order.invoice_number}",
                    amount =  order.payed_amount,
                    bill_number = order.invoice_number,
                    other = order.customer.name if order.customer else 'Cash Customer'
                
                )
            
            expense.save()   
    
    # Adjust stock
    try:
        if order.save_status == False:
            order.adjust_stock()  # Deduct the stock
            order.save_status = True
            order.save()
            return redirect("POS",pk = order_id)

        else:
            messages.info(request,"Cannot be save it is alredy saved the item")

            return redirect("POS",pk = order_id)
    except ValueError as e:
        messages.info(request,"Not Enough stock...")
        return redirect("POS",pk = order_id)
    
from io import BytesIO

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def change_invoice_date(request,pk):
    order = get_object_or_404(Order, id= pk)
    if request.method =="POST":
        date = request.POST.get("date")
        order.order_date = date
        order.save()
        messages.success(request, 'Order Date Changed')
        return redirect("POS",pk = pk)

from num2words import num2words

def amount_in_words(amount):
    # Split amount into whole and decimal parts
    whole_part = int(amount)
    decimal_part = int(round((amount - whole_part) * 100))
    
    # Convert each part to words
    whole_part_words = num2words(whole_part, lang='en')
    decimal_part_words = num2words(decimal_part, lang='en')
    
    # Combine with custom currency terms
    return f"{whole_part_words.capitalize()} Qathery Riyals and {decimal_part_words.capitalize()} Dirhams Only"

@login_required(login_url='SignIn')
def invoice_old(request,pk):
    order = get_object_or_404(Order, id=pk)
    
    # Save the order and calculate totals
    order.update_totals()
    order.calculate_balance()
    order_items = order.orderitem_set.all()
    # Adjust stock
    # try:
    #     if order.save_status == False:
    #         order.adjust_stock()  # Deduct the stock
    #         order.save_status = True
    #         order.save()

    #     if Income.objects.filter(bill_number = order.invoice_number).exists():
    #         expense = Income.objects.filter(bill_number = order.invoice_number)
    #         total = 0
            
    #         for ex in expense:
    #             total = total + ex.amount
            
    #         amount = order.payed_amount - total
    #         if amount > 0:
    #             expense = Income(
    #                 perticulers = f"Amount Against order {order.invoice_number}",
    #                 amount =  amount,
    #                 bill_number = order.invoice_number,
    #                 other = order.customer.name if order.customer else 'Cash Customer'
                
    #             )
            
    #             expense.save() 
    #     else:
    #         expense = Income(
    #                 perticulers = f"Amount Against order {order.invoice_number}",
    #                 amount =  order.payed_amount,
    #                 bill_number = order.invoice_number,
    #                 other = order.customer.name if order.customer else 'Cash Customer'
                
    #             )
            
    #         expense.save()

        # order = Order.objects.get(pk=pk)
        # context = {
        #     'order': order
        # }
        # pdf = render_to_pdf('invoice_template.html', context)
        # if pdf:
        #     return HttpResponse(pdf, content_type='application/pdf')
        # return HttpResponse("Error generating PDF")

        
    context = {
    "order": order,
    "order_items": order_items,
    "total_in_words": amount_in_words(round(order.total_amount,2))
    }
    return render(request,'invoice_template.html',context)

      # Get all OrderItems for the specific order
    # except ValueError as e:
    #     messages.info(request,"Not Enough stock...")
    #     return redirect("POS",pk = pk)


from math import ceil

@login_required(login_url='SignIn')
def invoice(request, pk):
    order = get_object_or_404(Order, id=pk)
    order_items = list(order.orderitem_set.all())

    # Paginate items: 20 items per page
    items_per_page = 20
    total_pages = ceil(len(order_items) / items_per_page)
    paginated_items = [
        order_items[i * items_per_page:(i + 1) * items_per_page]
        for i in range(total_pages)
    ]
      # Add sequential numbers to each item
    for page_index, page in enumerate(paginated_items, start=1):
        forloop_offset = (page_index - 1) * items_per_page
        for i, item in enumerate(page, start=1):
            item.sequential_number = forloop_offset + i

    # Pass the necessary context to the template
    context = {
        "order": order,
        "paginated_items": paginated_items,  # A list of pages, each containing items
        "total_in_words": amount_in_words(round(order.total_amount, 2)),  # Convert total amount to words
        "items_per_page": items_per_page,
        "total_pages": total_pages,
    }
    return render(request, 'invoice_template.html', context)


# @csrf_exempt
# def update_order_payment(request, order_id):
#     if request.method == 'POST':
#         order = Order.objects.get(id=order_id)
#         payed_amount = float(request.POST.get('payed_amount', 0))
#         discount = float(request.POST.get('discount', 0))

#         # Update the order
#         order.payed_amount = payed_amount
#         order.discount = discount
#         order.total_amount -= order.discount
#         order.calculate_balance()
        
#          # Render the order items table
#         order_items_html = render_to_string('ajaxtemplates/order_items_table.html', {'order': order})
#         return JsonResponse({"success": True, "html": order_items_html})
        
#     return JsonResponse({"success": False, "error": "Invalid request"})


def AddDiscount(request):
    return render(request,"add-discount.html")


def Listdiscount(request):
    return render(request,"list-discount.html")



# returns calculations


def list_returns(request):
    returns = Returns.objects.all()

    context = {
        "returns":returns
    }
    return render(request,"returns/list-returns.html",context)


def add_returns(request):
    return render(request,"returns/add-returns.html")



def fetch_order_items(request):
    if request.method == "POST":
        order_number = request.POST.get("order_number")
        
        # Fetch the order by invoice number
        try:
            order = Order.objects.get(invoice_number=order_number)
            order_items = order.orderitem_set.all() 
            customer = order.customer # Retrieve related order items
        except Order.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)

        # Render the `returnitemtable.html` with the fetched items
        html = render(request, 'ajaxtemplates/returnitemtable.html', {
            'order_items': order_items,
            "customer":customer,
            "order":order
        }).content.decode('utf-8')

        # Return HTML to be inserted in #itemtable
        return JsonResponse({'html': html})
    return JsonResponse({"error": "Invalid request"}, status=400)


def create_return_on_purchase(request, pk, item_id):
    order = Order.objects.get(id = pk)
    item = OrderItem.objects.get(id = item_id)
    print(order, item)
    if ReturnOrderItem.objects.filter(order_item = item).exists():
        Ritem = ReturnOrderItem.objects.filter(order_item = item).first()
        returns = Ritem.return_number
        return redirect('single_returns',pk =  returns.id)
    else:
        returns = Returns(
            order = order,
            reason = "Returns"
        )
        returns.save()
        return_item = ReturnOrderItem.objects.create(order_item = item ,return_quantity = 1 , return_number = returns,reason = "Sale Return" )
        return_item.save()
        return redirect("single_returns",pk = returns.id)

    


def single_returns(request,pk):
    returns = Returns.objects.get(id = pk)
    return_item = ReturnOrderItem.objects.get(return_number = returns)
    return render(request,"returns/return_single.html",{
        "return_item":return_item,
        "returns":returns
    })

def ItemPOST(request, pk, item_id):
    returns = Returns.objects.get(id = pk)
    return_item = ReturnOrderItem.objects.get(id = item_id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity"))
        reason = request.POST.get("reason")
        if quantity <= return_item.order_item.quantity:
            return_item.return_quantity = quantity
            return_item.reason = reason
            return_item.save()
            returns.confirmation = True
            returns.save()
            messages.info(request,"Return Confirmed......")
            return redirect("single_returns",pk = returns.id)
        else:
            messages.info(request,"No Sufficient items purchased")
            return redirect("single_returns",pk = returns.id)








