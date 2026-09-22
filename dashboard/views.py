from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import Order


# Create your views here.
@login_required
def dashboard(request):
    owner = request.user.owner
    orders = Order.objects.filter(owner=owner)
    order_count = orders.count()
    pending_orders = orders.exclude(status="Delivered").count()

    return render(
        request,
        "index.html",
        {
            "orders": orders,
            "pending_orders": pending_orders,
            "orders_count": order_count,
        },
    )
