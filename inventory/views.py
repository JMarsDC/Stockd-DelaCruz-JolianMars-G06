from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required

from .forms import StorageForm
from .models import Storage

ALL_ROLES = ("admin", "customer")


@role_required(*ALL_ROLES)
def storage_list(request):
    storages = Storage.objects.filter(owner=request.user)
    return render(request, "inventory/storage_list.html", {"storages": storages})


@role_required(*ALL_ROLES)
def storage_detail(request, pk):
    if request.user.role == "admin":
        storage = get_object_or_404(Storage, pk=pk)
    else:
        storage = get_object_or_404(Storage, pk=pk, owner=request.user)
    context = {"storage": storage, "is_owner": storage.owner == request.user}
    return render(request, "inventory/storage_detail.html", context)


@role_required(*ALL_ROLES)
def storage_create(request):
    form = StorageForm(request.POST or None, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            storage = form.save(commit=False)
            storage.owner = request.user
            storage.save()
            messages.success(request, f'Storage "{storage.name}" created.')
            return redirect("storage_detail", pk=storage.pk)
        messages.error(request, "Please fix the errors below.")
    return render(request, "inventory/storage_form.html", {"form": form, "mode": "Create"})


@role_required(*ALL_ROLES)
def storage_edit(request, pk):
    storage = get_object_or_404(Storage, pk=pk, owner=request.user)
    form = StorageForm(request.POST or None, instance=storage, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f'Storage "{storage.name}" updated.')
            return redirect("storage_detail", pk=storage.pk)
        messages.error(request, "Please fix the errors below.")
    return render(request, "inventory/storage_form.html", {"form": form, "mode": "Edit"})


@role_required(*ALL_ROLES)
def storage_delete(request, pk):
    storage = get_object_or_404(Storage, pk=pk, owner=request.user)
    if request.method == "POST":
        name = storage.name
        storage.delete()
        messages.success(request, f'Storage "{name}" and its items were deleted.')
        return redirect("storage_list")
    return render(request, "inventory/storage_confirm_delete.html", {"storage": storage})