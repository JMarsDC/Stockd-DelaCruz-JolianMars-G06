from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from accounts.decorators import role_required
from inventory.models import Item, Storage


@login_required
def dashboard_redirect(request):
    if request.user.role == "admin":
        return redirect("admin_dashboard")
    return redirect("customer_dashboard")


@role_required("admin")
def admin_dashboard(request):
    User = get_user_model()
    context = {
        "total_users": User.objects.count(),
        "total_storages": Storage.objects.count(),
        "total_items": Item.objects.count(),
        "my_storage_count": Storage.objects.filter(owner=request.user).count(),
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@role_required("customer")
def customer_dashboard(request):
    storages = Storage.objects.filter(owner=request.user)
    items = Item.objects.filter(owner=request.user)
    soon = timezone.localdate() + timedelta(days=7)
    context = {
        "storage_count": storages.count(),
        "item_count": items.count(),
        "recent_storages": storages.order_by("-created_at")[:5],
        "expiring_items": items.filter(expiry_date__isnull=False, expiry_date__lte=soon)
        .select_related("storage")[:5],
    }
    return render(request, "dashboard/customer_dashboard.html", context)