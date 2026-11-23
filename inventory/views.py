from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required

from .forms import StorageForm, ItemForm
from .models import Storage, Item

ALL_ROLES = ("admin", "customer")


@role_required(*ALL_ROLES)
def storage_list(request):
    storages = Storage.objects.filter(owner=request.user).annotate(item_count=Count("items"))
    return render(request, "inventory/storage_list.html", {"storages": storages})


@role_required(*ALL_ROLES)
def storage_detail(request, pk):
    if request.user.role == "admin":
        storage = get_object_or_404(Storage, pk=pk)
    else:
        storage = get_object_or_404(Storage, pk=pk, owner=request.user)
    context = {
        "storage": storage,
        "items": storage.items.all(),
        "is_owner": storage.owner == request.user,
    }
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



@role_required(*ALL_ROLES)
def item_add(request, storage_pk):
    storage = get_object_or_404(Storage, pk=storage_pk, owner=request.user)
    form = ItemForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            item = form.save(commit=False)
            item.storage = storage
            item.owner = request.user
            item.save()
            messages.success(request, f'"{item.name}" added to {storage.name}.')
            return redirect("storage_detail", pk=storage.pk)
        messages.error(request, "Please fix the errors below.")
    return render(request, "inventory/item_form.html", {"form": form, "storage": storage, "mode": "Add"})


@role_required(*ALL_ROLES)
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    form = ItemForm(request.POST or None, instance=item)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f'"{item.name}" updated.')
            return redirect("storage_detail", pk=item.storage_id)
        messages.error(request, "Please fix the errors below.")
    return render(request, "inventory/item_form.html", {"form": form, "storage": item.storage, "mode": "Edit"})


@role_required(*ALL_ROLES)
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    storage_pk = item.storage_id
    if request.method == "POST":
        name = item.name
        item.delete()
        messages.success(request, f'"{name}" was deleted.')
        return redirect("storage_detail", pk=storage_pk)
    return render(request, "inventory/item_confirm_delete.html", {"item": item})


@role_required("admin")
def all_storages(request):
    storages = Storage.objects.select_related("owner").annotate(item_count=Count("items"))
    return render(request, "inventory/all_storages.html", {"storages": storages})