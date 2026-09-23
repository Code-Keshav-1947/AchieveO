import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Order
from .forms import OrderForm
from customers.models import Customer
from products.models import Product
from owners.utils import get_current_owner


@login_required
def order_list(request):
    owner = get_current_owner(request.user)
    orders = Order.objects.filter(owner=owner).select_related("product", "customer")

    # Filters
    q = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip().lower()
    pay_filter = request.GET.get("payment", "").strip().lower()

    if q:
        orders = orders.filter(
            name__icontains=q
        ) | orders.filter(
            customer__name__icontains=q
        ) | orders.filter(
            product__name__icontains=q
        )

    if status_filter:
        orders = orders.filter(status__iexact=status_filter)

    # Filter payment in memory or queryset
    if pay_filter:
        filtered_orders = []
        for o in orders:
            if o.payment_status == pay_filter:
                filtered_orders.append(o)
        orders = filtered_orders

    customers = Customer.objects.filter(owner=owner)
    products = Product.objects.filter(owner=owner)
    form = OrderForm(owner=owner)

    return render(
        request,
        "orders/order_list.html",
        {
            "orders": orders,
            "customers": customers,
            "products": products,
            "form": form,
            "q": q,
            "status_filter": status_filter,
            "pay_filter": pay_filter,
            "status_choices": Order.STATUS,
            "active_tab": "orders",
        },
    )


@login_required
def order_create(request):
    owner = get_current_owner(request.user)
    if request.method == "POST":
        form = OrderForm(request.POST, owner=owner)
        if form.is_valid():
            order = form.save(commit=False)
            order.owner = owner
            # Double check product and customer belong to owner
            if order.customer.owner != owner or order.product.owner != owner:
                return JsonResponse({"status": "error", "message": "Invalid customer or product selected."}, status=400)
            order.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.GET.get("format") == "json":
                return JsonResponse({
                    "status": "success",
                    "id": order.id,
                    "name": order.name,
                    "customer_name": order.customer.name,
                    "product_name": order.product.name,
                    "quantity": order.quantity,
                    "total_amount": order.total_amount,
                    "advance": order.advance,
                    "balance": order.balance,
                    "payment_status": order.payment_status,
                    "order_status": order.status,
                })

            messages.success(request, f"Order #{order.id} for '{order.customer.name}' created successfully!")
            return redirect("dashboard")
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.GET.get("format") == "json":
                return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    else:
        form = OrderForm(owner=owner)

    return render(request, "orders/order_form.html", {"form": form, "active_tab": "orders"})


@login_required
def order_edit(request, pk):
    owner = get_current_owner(request.user)
    order = get_object_or_404(Order, pk=pk, owner=owner)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order, owner=owner)
        if form.is_valid():
            form.save()
            messages.success(request, f"Order #{order.id} updated successfully!")
            return redirect("dashboard")
    else:
        form = OrderForm(instance=order, owner=owner)

    return render(request, "orders/order_form.html", {"form": form, "order": order, "active_tab": "orders"})


@login_required
def order_delete(request, pk):
    owner = get_current_owner(request.user)
    order = get_object_or_404(Order, pk=pk, owner=owner)

    if request.method == "POST":
        order_num = order.id
        order.delete()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": "success", "id": order_num})
        messages.success(request, f"Order #{order_num} deleted successfully!")
        return redirect("dashboard")

    return render(request, "orders/order_confirm_delete.html", {"order": order, "active_tab": "orders"})


@login_required
@require_POST
def order_update_status(request, pk):
    owner = get_current_owner(request.user)
    order = get_object_or_404(Order, pk=pk, owner=owner)
    new_status = request.POST.get("status", "").strip().lower()

    valid_statuses = [s[0] for s in Order.STATUS]
    if new_status in valid_statuses:
        order.status = new_status
        order.save()
        return JsonResponse({
            "status": "success",
            "id": order.id,
            "new_status": order.status,
            "status_display": order.get_status_display(),
        })
    return JsonResponse({"status": "error", "message": "Invalid status value."}, status=400)


@login_required
def order_invoice(request, pk):
    owner = get_current_owner(request.user)
    order = get_object_or_404(Order, pk=pk, owner=owner)
    return render(request, "orders/invoice.html", {"order": order, "owner": owner})


@login_required
def order_export_csv(request):
    owner = get_current_owner(request.user)
    orders = Order.objects.filter(owner=owner).select_related("product", "customer")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="orders_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Order ID", "Date", "Customer Name", "Customer Phone",
        "Job Name", "Product", "Quantity", "Unit Price (INR)",
        "Total Amount (INR)", "Advance Paid (INR)", "Balance Due (INR)",
        "Payment Status", "Order Status", "Due Date", "Notes"
    ])

    for o in orders:
        writer.writerow([
            f"#{o.id}",
            o.date_get.strftime("%Y-%m-%d") if o.date_get else "",
            o.customer.name,
            o.customer.mobile_no or "",
            o.name,
            o.product.name,
            o.quantity,
            o.product.price,
            o.total_amount,
            o.advance,
            o.balance,
            o.payment_status.title(),
            o.get_status_display(),
            o.due_date.strftime("%Y-%m-%d") if o.due_date else "",
            o.notes or "",
        ])

    return response
