from django.shortcuts import redirect, render
from .models import Order, Product

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    quantity_from_form = int(request.POST["quantity"])
    purchased_item_id = request.POST['product_id']
    price_of_item = float(Product.objects.get(id=purchased_item_id).price)
    total_charge = quantity_from_form * price_of_item
    request.session['total_charge'] = total_charge
    print("Charging credit card...")
    Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
    if 'total_spent' not in request.session:
        request.session['counter'] = 0
        request.session['total_spent'] = 0
    request.session['counter'] += quantity_from_form
    request.session['total_spent'] += total_charge
    return redirect("/checkout_page")

def only_summary(request):
    context = {
        'total_charge': request.session['total_charge'],
        'current_count': request.session['counter'],
        'total_spent': request.session['total_spent']
    }
    return render(request,'store/checkout.html', context)