from django.shortcuts import render , redirect , HttpResponse
from expense_tracker.models import *
from django.db.models import Sum


### code khrab nahi hojayega?

# Create your views here.
def register(request):
    return render(request , 'register.html')

def regi(request):
      if request.method == 'POST':
        name = request.POST['user_name']
        email = request.POST['user_email']
        password = request.POST['user_pass']

        if user.objects.filter(email=email).exists():
            data = {'email': email, 'message': "User Already exists. Please Login."}
            return render(request, 'login.html', {'data': data})

        u = user.objects.create(name=name, email=email, password=password)
        exp = expense.objects.filter(user=u)
        return render(request, 'welcome.html', {'u': u, 'expense': exp, 'total': 0})

    # If the request method is not POST, redirect to some appropriate URL
        return redirect('')  # You might want to change this redirection to suit your application

def login(request):
    return render(request , 'login.html')

def logi(request):
     if request.method == 'POST':
        email = request.POST['user_email']
        password = request.POST['user_pass']
        
        if user.objects.filter(email=email, password=password).exists():
            u = user.objects.get(email=email)
            exp = expense.objects.filter(user=u)
            total_expense = expense.objects.filter(user=u).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
            return render(request, 'welcome.html', {'u': u, 'expense': exp, 'total': total_expense})
        
        data = {'message': "Wrong password or user does not exist."}
        return render(request, 'login.html', {'data': data})

    # If the request method is not POST, redirect to some appropriate URL
     return redirect('')  # You might want to change this redirection to suit your application

def show(request ):
    u = user.objects.all()
    return render(request , 'show.html' , {'db':u})


def addTransaction(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        description = request.POST.get('expense_name')
        amount = request.POST.get('amount')

        u = user.objects.get(email=email)

        if expense.objects.filter(user=u, expense_name=description).exists():
            # If description already exists for the same user
            obj = expense.objects.get(user=u, expense_name=description)
            obj.amount += int(amount)
            obj.save()
        else:
            exp = expense(expense_name=description, amount=amount, user=u)
            exp.save()

        user_obj = user.objects.get(email=email)
        db = expense.objects.filter(user=user_obj).values()
        total_expense = expense.objects.filter(user=user_obj).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        return render(request, 'welcome.html', {'u': user_obj, 'expense': db, 'total': total_expense})


    # If the request method is not POST, redirect to some appropriate URL
        return redirect('')  # You might want to change this redirection to suit your application



def delete_transaction(request , id):
        u = expense.objects.get(id = id)
        email = u.user.email
        u.delete()
        user_obj = user.objects.get(email=email)
        db = expense.objects.filter(user=user_obj).values()
        total_expense = expense.objects.filter(user=user_obj).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        return render(request, 'welcome.html', {'u': user_obj, 'expense': db, 'total': total_expense})


def editTransaction(request , id):
    new_description = request.GET['expense_name']
    new_amount = request.GET['amount']
    u = expense.objects.get(id= id)
    u.expense_name = new_description
    u.amount = new_amount
    u.save()
    email = u.user.email
    user_obj = user.objects.get(email=email)
    db = expense.objects.filter(user=user_obj).values()
    total_expense = expense.objects.filter(user=user_obj).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    return render(request, 'welcome.html', {'u': user_obj, 'expense': db, 'total': total_expense})
