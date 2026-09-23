from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import Order
from customers.models import Customer
from products.models import Product
from owners.utils import get_current_owner


@login_required
def dashboard(request):
    owner = get_current_owner(request.user)
    orders = Order.objects.filter(owner=owner).select_related("product", "customer")
    customers = Customer.objects.filter(owner=owner)
    products = Product.objects.filter(owner=owner)

    orders_count = orders.count()
    pending_orders = orders.exclude(status="delivered").count()
    total_amount = sum(o.total_amount for o in orders)
    estimated_profit = sum(o.estimated_profit for o in orders)
    total_balance = sum(o.balance for o in orders)
    total_received = sum(o.advance for o in orders)

    # Status breakdown for Kanban board
    status_choices = Order.STATUS
    kanban_lanes = [
        {
            "code": code,
            "label": label,
            "orders": [o for o in orders if o.status.lower() == code.lower()],
        }
        for code, label in status_choices
    ]

    context = {
        "orders": orders,
        "customers": customers,
        "products": products,
        "orders_count": orders_count,
        "pending_orders": pending_orders,
        "total_amount": total_amount,
        "estimated_profit": estimated_profit,
        "total_balance": total_balance,
        "total_received": total_received,
        "status_choices": status_choices,
        "kanban_lanes": kanban_lanes,
        "active_tab": "dashboard",
    }

    return render(request, "index.html", context)

