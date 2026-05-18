from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from products.models import Product
from .models import Order, OrderItem


# ---------------- HOME ----------------

def home(request):

    return render(request, 'home.html')


# ---------------- PRODUCTS ----------------

@login_required(login_url='/login/')
def products_view(request):

    products = Product.objects.all()

    return render(
        request,
        'products.html',
        {
            'products': products
        }
    )


# ---------------- ADD TO CART ----------------

@login_required(login_url='/login/')
def add_to_cart(request):

    product_id = str(request.GET.get('id'))

    quantity = int(request.GET.get('qty'))

    cart = request.session.get('cart', {})

    if product_id in cart:

        cart[product_id] += quantity

    else:

        cart[product_id] = quantity

    request.session['cart'] = cart

    return redirect('/cart/')


# ---------------- CART ----------------

@login_required(login_url='/login/')
def cart_view(request):

    cart = request.session.get('cart', {})

    cart_items = []

    grand_total = 0

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        total_price = product.price * quantity

        grand_total += total_price

        cart_items.append({

            'product': product,

            'quantity': quantity,

            'total_price': total_price

        })

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'grand_total': grand_total
        }
    )


# ---------------- PLACE ORDER ----------------

@login_required(login_url='/login/')
def place_order(request):

    cart = request.session.get('cart', {})

    if not cart:

        return redirect('/cart/')

    grand_total = 0

    order = Order.objects.create(

        retailer=request.user,

        total_amount=0

    )


    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        total_price = product.price * quantity

        grand_total += total_price

        OrderItem.objects.create(

            order=order,

            product=product,

            quantity=quantity,

            total_price=total_price

        )

    order.total_amount = grand_total

    order.save()

    request.session['cart'] = {}

    # ---------------- EMAIL ----------------

    send_mail(

        'New Retail Order',

        f'''
Retailer: {request.user.username}

Order ID: {order.id}

Total Amount: ₹{order.total_amount}
''',

        None,

        ['pravalikakaithoju@gmail.com'],

        fail_silently=False

    )

    return render(
        request,
        'order_success.html',
        {
            'order': order
        }
    )


# ---------------- MY ORDERS ----------------

@login_required(login_url='/login/')
def my_orders(request):

    orders = Order.objects.filter(

        retailer=request.user

    ).order_by('-created_at')

    return render(
        request,
        'my_orders.html',
        {
            'orders': orders
        }
    )


# ---------------- ORDER DETAIL ----------------

@login_required(login_url='/login/')
def order_detail(request, order_id):

    order = Order.objects.get(

        id=order_id,

        retailer=request.user

    )

    items = OrderItem.objects.filter(

        order=order

    )

    return render(
        request,
        'order_detail.html',
        {
            'order': order,
            'items': items
        }
    )
@login_required(login_url='/login/')
def dashboard(request):

    total_orders = Order.objects.filter(
        retailer=request.user
    ).count()

    pending_orders = Order.objects.filter(
        retailer=request.user,
        status='Pending'
    ).count()

    delivered_orders = Order.objects.filter(
        retailer=request.user,
        status='Delivered'
    ).count()

    recent_orders = Order.objects.filter(
        retailer=request.user
    ).order_by('-created_at')[:5]

    return render(
        request,
        'dashboard.html',
        {
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'delivered_orders': delivered_orders,
            'recent_orders': recent_orders
        }
    )