from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from owners.utils import get_current_owner


@login_required
def product_list(request):
    owner = get_current_owner(request.user)
    query = request.GET.get("q", "").strip()
    products = Product.objects.filter(owner=owner)

    if query:
        products = products.filter(name__icontains=query)

    form = ProductForm()
    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "form": form,
            "query": query,
            "active_tab": "products",
        },
    )


@login_required
def product_create(request):
    owner = get_current_owner(request.user)
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = owner
            product.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.GET.get("format") == "json":
                return JsonResponse({
                    "status": "success",
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "cost_price": product.cost_price or 0,
                    "stocks": product.stocks or 0,
                })

            messages.success(request, f"Product '{product.name}' created successfully!")
            return redirect("product_list")
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.GET.get("format") == "json":
                return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    else:
        form = ProductForm()

    return render(request, "products/product_form.html", {"form": form, "active_tab": "products"})


@login_required
def product_edit(request, pk):
    owner = get_current_owner(request.user)
    product = get_object_or_404(Product, pk=pk, owner=owner)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully!")
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "products/product_form.html", {"form": form, "product": product, "active_tab": "products"})


@login_required
def product_delete(request, pk):
    owner = get_current_owner(request.user)
    product = get_object_or_404(Product, pk=pk, owner=owner)

    if request.method == "POST":
        name = product.name
        product.delete()
        messages.success(request, f"Product '{name}' deleted successfully!")
        return redirect("product_list")

    return render(request, "products/product_confirm_delete.html", {"product": product, "active_tab": "products"})
