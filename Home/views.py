from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import  messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unautenticated_user
from django.contrib.auth.decorators import login_required
import datetime
from Finance.models import Income, Expence
from django.db.models import Sum
from django.utils.timezone import now
from POS.models import Order
from Inventory.models import Product, Purchase
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from .models import Staff, StaffSalary, Notification
from .forms import StaffForm, StaffSalaryForm
import calendar
from datetime import timedelta
from django.core.cache import cache



def monthly_income_view():
    today = datetime.datetime.today()
    
    # Get the first and last day of the current month
    first_day_of_month = today.replace(day=1)
    next_month = first_day_of_month.replace(month=today.month % 12 + 1, day=1) if today.month != 12 else first_day_of_month.replace(year=today.year + 1, month=1)
    last_day_of_month = next_month - timedelta(days=1)

    # Get all income and expense entries for the current month
    income_entries = Income.objects.filter(date__range=[first_day_of_month, last_day_of_month])
    expense_entries = Expence.objects.filter(date__range=[first_day_of_month, last_day_of_month])

    # Calculate weekly income
    weekly_income = []
    weekly_expense = []
    current_start = first_day_of_month
    while current_start <= last_day_of_month:
        current_end = min(current_start + timedelta(days=6), last_day_of_month)

        # Income for the week
        weekly_total_income = income_entries.filter(date__range=[current_start, current_end]).aggregate(Sum('amount'))['amount__sum'] or 0
        weekly_income.append(weekly_total_income)

        # Expense for the week
        weekly_total_expense = expense_entries.filter(date__range=[current_start, current_end]).aggregate(Sum('amount'))['amount__sum'] or 0
        weekly_expense.append(weekly_total_expense)

        current_start = current_end + timedelta(days=1)

    # Pass the weekly income and expense data to the template
    
    
    

    return weekly_income, weekly_expense

def dashboard_view():
    from django.utils.timezone import now, timedelta
    from django.db.models.functions import ExtractMonth
    from django.db.models import Sum
    from POS.models import Order
    from Inventory.models import InventoryStock, Product, Purchase

    # Get current date and one year ago date
    current_date = now()
    one_year_ago = current_date - timedelta(days=365)

    # Group Orders, Products, Purchases, Inventory by month and calculate the sum of the transaction amounts
    orders_by_month = Order.objects.filter(order_date__gte=one_year_ago) \
        .annotate(month=ExtractMonth('order_date')) \
        .values('month') \
        .annotate(total=Sum('total_amount')) \
        .order_by('month')

    purchases_by_month = Purchase.objects.filter(bill_date__gte=one_year_ago) \
        .annotate(month=ExtractMonth('bill_date')) \
        .values('month') \
        .annotate(total=Sum('purchase_price')) \
        .order_by('month')

    products_by_month = Product.objects.filter(create_date__gte=one_year_ago) \
        .annotate(month=ExtractMonth('create_date')) \
        .values('month') \
        .annotate(total=Sum('unit_price')) \
        .order_by('month')

    inventory_by_month = InventoryStock.objects.filter(date_added__gte=one_year_ago) \
        .annotate(month=ExtractMonth('date_added')) \
        .values('month') \
        .annotate(total=Sum('last_purchase_amount')) \

    # Data for each month (Jan - Dec, or 1 - 12)
    months = range(1, 13)
    orders_data = {item['month']: item['total'] or 0 for item in orders_by_month}
    purchases_data = {item['month']: item['total'] or 0 for item in purchases_by_month}
    products_data = {item['month']: item['total'] or 0 for item in products_by_month}
    inventory_data = {item['month']: item['total'] or 0 for item in inventory_by_month}

    # Ensure zero values for missing months
    orders_list = [orders_data.get(month, 0) for month in months]
    purchases_list = [purchases_data.get(month, 0) for month in months]
    products_list = [products_data.get(month, 0) for month in months]
    inventory_list = [inventory_data.get(month, 0) for month in months]

    # Pass data to the template (as lists, not tuples)
    return orders_list, purchases_list, products_list, inventory_list

def get_current_month_income_and_expense():
    # Get current year and month
    today = datetime.date.today()
    current_month_start = today.replace(day=1)
    current_month_end = (today.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
    
    # Filter and aggregate total income for the current month
    total_income = Income.objects.filter(
        date__gte=current_month_start,
        date__lte=current_month_end
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Filter and aggregate total expenses for the current month
    total_expense = Expence.objects.filter(
        date__gte=current_month_start,
        date__lte=current_month_end
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return total_income, total_expense


def get_current_month_orders():
    # Get current year and month
    today = datetime.date.today()
    current_month_start = today.replace(day=1)
    current_month_end = (today.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)

    # Filter orders for the current month and count them gunicorn Beta_POS.wsgi:application
    total_orders = Order.objects.filter(
        order_date__gte=current_month_start,
        order_date__lte=current_month_end
    ).count()

    return total_orders

def get_top_selling_products():
    # Annotate the total quantity sold for each product through OrderItem
    top_products = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')  # Sum quantity from related OrderItem model
    ).order_by('-total_sold')[:5]  # Order by total_sold in descending order and limit to 5

    return top_products


# for chat js function 

def get_monthly_data(request):
    # Get data for Orders grouped by month
    order_data = Order.objects.annotate(month=TruncMonth('order_date')).values('month').annotate(
        total_order_amount=Sum('total_amount')).order_by('month')

    # Get data for Purchases grouped by month
    purchase_data = Purchase.objects.annotate(month=TruncMonth('bill_date')).values('month').annotate(
        total_purchase_amount=Sum('amount')).order_by('month')

    # Prepare data for response
    response_data = {
        "months": [order['month'].strftime("%B %Y") for order in order_data],
        "orders": [order['total_order_amount'] for order in order_data],
        "purchases": [purchase['total_purchase_amount'] for purchase in purchase_data],
    }

    return JsonResponse(response_data)

def get_monthly_revenue_expense(request):
    # Aggregate Income data by month
    income_data = Income.objects.annotate(month=TruncMonth('date')).values('month').annotate(
        total_income=Sum('amount')).order_by('month')

    # Aggregate Expence data by month
    expense_data = Expence.objects.annotate(month=TruncMonth('date')).values('month').annotate(
        total_expense=Sum('amount')).order_by('month')

    # Prepare response data (months, income, expense)
    response_data = {
        "months": [income['month'].strftime("%B %Y") for income in income_data],
        "incomes": [income['total_income'] for income in income_data],
        "expenses": [expense['total_expense'] for expense in expense_data],
    }

    return JsonResponse(response_data)

@login_required(login_url='SignIn')
def Index(request):
    month = now().strftime("%B")
    
    total_income, total_expense = get_current_month_income_and_expense()
    total_orders = get_current_month_orders()
    top_products = get_top_selling_products()
    weekly_income,weekly_expense = monthly_income_view()
    orders, purchases, products, inventory = dashboard_view()

    # calculating totals of balance amount with caching method 
    # Attempt to retrieve the cached total balance
    total_balance = cache.get('total_balance')

    if total_balance is None:
        # If not cached, calculate and cache the total balance
        total_balance = Order.objects.aggregate(
            total_balance=Sum('balance_amount')
        )['total_balance'] or 0  # Default to 0 if no orders

        # Cache the result for 10 minutes (600 seconds)
        cache.set('total_balance', total_balance, 600)
    context = {
        "total_income":total_income,
        "total_expense":total_expense,
        "total_orders":total_orders,
        "top_products":top_products,
        "weekly_income":weekly_income,
        "weekly_expense":weekly_expense,
        "month":month,
        "orders":orders,
        "purchases":purchases,
        "products":products,
        "inventory":inventory,
        'total_balance': total_balance,
        

    }
    return render(request,"index.html",context)


@unautenticated_user
def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            
            request.session['username'] = username
            request.session['password'] = password
            login(request, user1)
            return redirect('Index')
        
        else:
            messages.error(request,'Username or Password Incorrect')
            return redirect('SignIn')
    return render(request,"login.html")


def SignOut(request):
    logout(request)
    return redirect('SignIn')


@login_required(login_url='SignIn')
def profile(request):
    if request.method == "POST":
        opass = request.POST.get("opswd")
        pswd = request.POST.get("pswd")
        cpswd = request.POST.get("cpswd")

        # Get current user
        user = request.user

        # Check if old password is correct
        if user.check_password(opass):
            # Check if new password and confirm password match
            if pswd == cpswd:
                # Set the new password
                user.set_password(pswd)
                user.save()
                
                # Re-authenticate and log the user back in
                user = authenticate(username=user.username, password=pswd)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Password changed successfully.")
                    return redirect("profile")
            else:
                messages.error(request, "Passwords do not match.")
                return redirect("profile")

        else:
            messages.error(request, "Old password is incorrect.")
            return redirect("profile")


    return render(request, "profile.html")

# In views.py
from django.shortcuts import render

def custom_500(request):
    return render(request, 'errorpage/pages-error-500.html', status=404)

def custom_404(request, exception):
    return render(request, 'errorpage/pages-error.html', status=500)


def add_customers(request):
    return render(request, "add_customers.html")



@login_required(login_url="SignIn")
def list_staff(request):
    staff = Staff.objects.all()

    context = {
        "staff":staff
    }
    return render(request,"list-staff.html",context)


@login_required(login_url="SignIn")
def add_staff(request):
    form = StaffForm()
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Staff Created Success.....")
            return redirect("list_staff")
    context = {
        "form":form
    }
    return render(request,"add-staff.html",context)


@login_required(login_url="SignIn")
def delete_staff(request,pk):
    staff = get_object_or_404(Staff,id = pk)
    staff.delete()
    messages.success(request,"employee deleted success.....")
    return redirect("list_staff")


@login_required(login_url="SignIn")
def update_staff(request,pk):
    staff = get_object_or_404(Staff,id = pk)
    salary = StaffSalary.objects.filter(staff = staff)
    form = StaffForm(instance=staff)
    if request.method == "POST":
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.info(request,"Staff Updated")
            return redirect("list_staff")
    
    return render(request,"update_staff.html",{"form":form, "staff":staff,"salary":salary})




# finance salary calculation associated functions gos here

@login_required(login_url="SignIn")
def list_salary(request):
    salary = StaffSalary.objects.all()
    return render(request,"list-salaries.html",{"salary":salary})

@login_required(login_url="SignIn")
def add_salary(request):
    form = StaffSalaryForm()
    if request.method == "POST":
        form = StaffSalaryForm(request.POST)
        if form.is_valid():
            salary = form.save()
            salary.save()
            expense = Expence(
                        perticulers = f"Paid to  {salary.staff} as Salary Slip No {salary.slip_no}",
                        date = datetime.datetime.now(),
                        amount = salary.amount
                    )
            expense.save()
            messages.success(request,"Salary was added to Staff account")
            return redirect("list_salary")
        else:
            messages.error(request,"Some thing Wrong")
            return redirect("list_salary")
        
    return render(request,"add-salary.html",{"form":form})


def delete_staff_salary(request,pk):
    salary = get_object_or_404(StaffSalary,id = pk)
    salary.delete()
    messages.success(request,"Salary deleted")
    return redirect("list_salary")

def notification_read(request,pk):
    notification = Notification.objects.get(id = pk)
    notification.is_read = True
    notification.save()
    return redirect("list_inventory")


def clear_notification(request):
    Notification.objects.all().delete()
    return redirect("Index")




