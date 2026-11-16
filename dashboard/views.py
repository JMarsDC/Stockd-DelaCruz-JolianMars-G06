from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.decorators import role_required


@login_required
def dashboard_redirect(request):
    if request.user.role == "admin":
        return redirect("admin_dashboard")
    return redirect("customer_dashboard")


@role_required("admin")
def admin_dashboard(request):
    return render(request, "dashboard/admin_dashboard.html")


@role_required("customer")
def customer_dashboard(request):
    return render(request, "dashboard/customer_dashboard.html")