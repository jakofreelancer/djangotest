from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory
from .filters import OrderFilter

#myFilter = OrderFilter()

# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivery').count()
    pending = orders.filter(status='Pending').count()

    context = {	'orders':orders, 
				'customers':customers, 
				'total_orders':total_orders,
				'delivered':delivered,
				'pending':pending}

    #return HttpResponse('Home Page')
    return render(request, 'dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products':products})

def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = Order.objects.all().filter(customer_id=pk_test)
    orders_count = orders.count()
	myFilter = OrderFilter(request.GET, queryset=orders)
	#orders = customer.order_set.all()
	#context = {'customer':customer}
    #, 'orders':orders}
    #, 'order_count':order_count}
    return render(request, 'customer.html', {'customer':customer,'orders':orders, 'orders_count':orders_count
	#,'myFilter':myFilter
	})

# def createOrder(request):
# 	form = OrderForm()
# 	if request.method == 'POST':
# 		#print('Printing POST:', request.POST)
# 		form = OrderForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('/')

# 	context = {'form':form}
# 	return render(request, 'order_form.html', context)

def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'order_form.html', context)

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'delete.html', context)

def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=30)
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset,'var1': Order.objects.get(id=1)}
	return render(request, 'order_form.html', context)