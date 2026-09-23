from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm
from owners.utils import get_current_owner


@login_required
def customer_list(request):
    owner = get_current_owner(request.user)
    query = request.GET.get("q", "").strip()
    customers = Customer.objects.filter(owner=owner).prefetch_related("orders")

    if query:
        customers = customers.filter(name__icontains=query) | customers.filter(mobile_no__icontains=query) | customers.filter(email__icontains=query)

    form = CustomerForm()
    return render(
        request,
        "customers/customer_list.html",
        {
            "customers": customers,
            "form": form,
            "query": query,
            "active_tab": "customers",
        },
    )


@login_required
def customer_create(request):
    owner = get_current_owner(request.user)
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.owner = owner
            customer.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.GET.get("format") == "json":
                return JsonResponse({
                    "status": "success",
                    "id": customer.id,
                    "name": customer.name,
                    "mobile_no": customer.mobile_no or "",
                    "email": customer.email or "",
                })

            messages.success(request, f"Customer '{customer.name}' added successfully!")
            return redirect("customer_list")
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.GET.get("format") == "json":
                return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    else:
        form = CustomerForm()

    return render(request, "customers/customer_form.html", {"form": form, "active_tab": "customers"})


@login_required
def customer_edit(request, pk):
    owner = get_current_owner(request.user)
    customer = get_object_or_404(Customer, pk=pk, owner=owner)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer '{customer.name}' updated successfully!")
            return redirect("customer_list")
    else:
        form = CustomerForm(instance=customer)

    return render(request, "customers/customer_form.html", {"form": form, "customer": customer, "active_tab": "customers"})


@login_required
def customer_delete(request, pk):
    owner = get_current_owner(request.user)
    customer = get_object_or_404(Customer, pk=pk, owner=owner)

    if request.method == "POST":
        name = customer.name
        customer.delete()
        messages.success(request, f"Customer '{name}' deleted successfully!")
        return redirect("customer_list")

    return render(request, "customers/customer_confirm_delete.html", {"customer": customer, "active_tab": "customers"})
